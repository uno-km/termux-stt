# termux-stt 아키텍처 및 소스 코드 전수 기술 분석 보고서

본 문서는 안드로이드 Termux 및 ARM64 모바일 환경에 특화된 온디바이스 음성인식(STT) 및 화자 분리(Speaker Diarization) 프레임워크인 `termux-stt`의 전체 아키텍처, 설치 메커니즘, 실행 라이프사이클 및 전 모듈의 소스 코드를 체계적으로 분석하여 기록한 전수 가이드입니다.

---

## 1. 아키텍처 개요 및 설계 원칙

`termux-stt`는 안드로이드의 하드웨어 리소스 제약(메모리 부족, 백그라운드 Doze 모드, C-확장 모듈 컴파일 제약 등) 하에서 고신뢰성 음성 처리 파이프라인을 구축하기 위해 설계되었습니다.

```
+-------------------------------------------------------------------------------+
|                             User / CLI / API                                  |
|   (Python API: create_engine() / Node.js API / CLI: termux-stt transcribe)    |
+---------------------------------------+---------------------------------------+
                                        |
+---------------------------------------v---------------------------------------+
|                    Engine Abstraction & Registry Layer                        |
|                     (termux_stt.engine.EngineRegistry)                        |
+-----------+-------------------+-------------------+---------------------------+
            |                   |                   |
+-----------v-----------+ +-----v-----------+ +-----v-----------+ +-------------v---------------+
|     WhisperEngine     | |   VoskEngine    | |  SherpaEngine   | |        HybridEngine         |
|  (whisper.cpp Subproc)| |(CFFI/Kaldi CAPI)| |  (Zipformer ONNX| | (Vosk X-Vector + Whisper STT|
|  ARM NEON / Vulkan NGL| |sys.platform fix)| |   Subprocess)   | |    Pure-Python K-Means)     |
+-----------+-----------+ +-----+-----------+ +-----+-----------+ +-------------+---------------+
            |                   |                   |                           |
+-----------+-------------------+-------------------+---------------------------+
|                               Audio Processing Pipeline                       |
|   1. Audio Loader (Pure-Python wave / ffprobe)                                |
|   2. Preprocessor (FFmpeg: 16kHz, 1ch, PCM s16le WAV 변환 및 libbluray 복구)    |
|   3. VAD (Silero-VAD / EnergyVAD 에너지 기반 무음 분할)                           |
+---------------------------------------+---------------------------------------+
                                        |
+---------------------------------------v---------------------------------------+
|                            Platform / Hardware Layer                          |
|   - HardwareInfo (/proc/cpuinfo, big.LITTLE 스레드 자동 할당, NEON/FP16 검증) |
|   - MobileGuard (termux-wake-lock RAII 컨텍스트 매니저, 메모리 누수 감시)     |
|   - ProcessPool (Subprocess 프로세스 격리를 통한 네이티브 크래시 차단)        |
+---------------------------------------+---------------------------------------+
                                        |
+---------------------------------------v---------------------------------------+
|                             Export Formatting Layer                           |
|       (Text, JSON [json_export.py], SRT [srt.py], VTT [vtt.py], RTTM)         |
+-------------------------------------------------------------------------------+
```

### 핵심 설계 원칙
1. **프로세스 격리(Process Isolation)**: C/C++ 네이티브 런타임(`whisper.cpp`, `sherpa-onnx`) 구동 시 발생하는 세그멘테이션 폴트(SIGSEGV, -11)가 파이썬 프로세스를 다운시키지 않도록 서브프로세스 샌드박스 계층을 통해 실행을 격리하고 실패 시 자동 복구를 수행합니다.
2. **모바일 네이티브 의존성 최소화 (Pure-Python Zero-Heavy-Deps)**: 화자 클러스터링을 위해 무거운 `scikit-learn`이나 빌드가 불안정한 대형 C-확장 모듈 대신 순수 파이썬 K-Means 클러스터링 알고리즘을 독자 구현하여 런타임 메모리 풋프린트를 200MB 미만으로 억제합니다.
3. **플랫폼 스푸핑 및 안드로이드 예외 방어**:
   - Vosk 네이티브 라이브러리의 안드로이드 플랫폼 검증 오류를 우회하기 위해 `sys.platform = 'linux'` 스푸핑을 적용합니다.
   - 안드로이드의 루트 `/tmp` 읽기 전용 권한 오류를 방지하기 위해 `$TMPDIR` 또는 `~/tmp`로 출력 경로를 자동 우회합니다.
4. **하드웨어 가속 통합**: `ameva-vulkan-runtime`과 연동하여 GPU 레이어 오프로드(`-ngl`) 및 ARM NEON/FP16 벡터 연산을 활성화합니다.

---

## 2. 전체 디렉터리 및 모듈 구조

```
termux-stt/
├── bin/
│   └── termux-stt.js               # Node.js/NPX 실행 래퍼 진입점
├── lib/
│   ├── engine.js                   # Node.js 엔진 추상화 클래스 및 결과 모델
│   ├── hybrid.js                   # Node.js 하이브리드 엔진 바인딩
│   ├── vosk.js                     # Node.js Vosk 엔진 바인딩
│   └── whisper.js                  # Node.js Whisper 엔진 바인딩
├── scripts/
│   ├── download_models.sh          # 모델 일괄 다운로드 쉘 스크립트
│   ├── install_sherpa_onnx.sh      # Sherpa-ONNX 컴파일 및 설치 스크립트
│   ├── install_vosk.sh             # Vosk 런타임 환경 구성 스크립트
│   └── install_whisper_cpp.sh      # whisper.cpp 클론 및 NEON 빌드 스크립트
├── termux_stt/
│   ├── __init__.py                 # create_engine() 팩토리 및 공개 인터페이스
│   ├── __main__.py                 # python -m termux_stt 진입점
│   ├── audio/                      # 오디오 수집 및 전처리 서브패키지
│   │   ├── __init__.py
│   │   ├── loader.py               # Pure-Python wave 파서 및 ffprobe 메타데이터 로더
│   │   ├── mic.py                  # termux-microphone-record 연동 마이크 캡처
│   │   ├── preprocessor.py         # 16kHz mono PCM 변환 및 패키지 자동 복구
│   │   └── vad.py                  # EnergyVAD 및 음성 구간 분할
│   ├── cli/                        # CLI 서브커맨드 구현 서브패키지
│   │   ├── __init__.py
│   │   ├── benchmark.py            # RTF(Real Time Factor) 및 메모리 벤치마크
│   │   ├── diarize.py              # 화자 분리 실행 커맨드
│   │   ├── doctor.py               # 시스템 환경 및 의존성 진단 커맨드
│   │   ├── listen.py               # 실시간 마이크 청취 커맨드
│   │   ├── main.py                 # Argparse CLI 엔트리포인트
│   │   ├── models_cmd.py           # 모델 다운로드/목록 관리 커맨드
│   │   └── transcribe.py           # 파일 전사 커맨드
│   ├── diarization/                # 화자 분리 알고리즘 서브패키지
│   │   ├── __init__.py
│   │   ├── clustering.py           # Pure-Python K-Means 및 벡터 거리 연산
│   │   ├── mapper.py               # 시간 윈도우 기반 발화자-텍스트 정렬
│   │   └── xvector.py              # 128차원 화자 임베딩 데이터 모델
│   ├── engine/                     # STT 백엔드 엔진 서브패키지
│   │   ├── __init__.py             # EngineRegistry 지연 등록 팩토리
│   │   ├── base.py                 # Engine 기본 추상 클래스 및 EngineConfig
│   │   ├── hybrid_engine.py        # Vosk X-Vector + Whisper 결합 하이브리드 엔진
│   │   ├── sherpa_engine.py        # Sherpa-ONNX 오프라인 엔진
│   │   ├── vosk_engine.py          # Vosk CFFI/Kaldi STT 및 임베딩 엔진
│   │   └── whisper_engine.py       # whisper.cpp 서브프로세스 래퍼
│   ├── export/                     # 결과 포맷 변환 및 내보내기 서브패키지
│   │   ├── __init__.py
│   │   ├── json_export.py          # JSON 포맷 직렬화
│   │   ├── result.py               # Segment, TranscriptResult, DiarizedResult
│   │   ├── rttm.py                 # RTTM 표준 화자 분리 포맷 변환
│   │   ├── srt.py                  # SRT 자막 포맷 변환
│   │   └── vtt.py                  # WebVTT 자막 포맷 변환
│   ├── models/                     # 모델 허브 및 양자화 관리 서브패키지
│   │   ├── __init__.py
│   │   ├── hub.py                  # HTTP 스트리밍 다운로드 및 무결성 검증
│   │   ├── quantization.py         # GGML 양자화 규격 정의 및 메모리 기반 추천
│   │   └── registry.py             # 공식 지원 모델 메타데이터 카탈로그
│   └── platform/                   # 플랫폼 적응 및 모바일 가드 서브패키지
│       ├── __init__.py
│       ├── hardware.py             # CPU, 메모리, NEON/FP16 하드웨어 탐지
│       ├── installer.py            # 1-Click 자동 의존성 프로비저닝 엔진
│       ├── mobile_guard.py         # WakeLock RAII 가드 및 Doze 방지
│       └── process_pool.py         # 서브프로세스 격리 및 크래시 자동 재시도
├── package.json                    # Node.js NPM 패키지 메타데이터 (v1.1.3)
├── pyproject.toml                  # PEP 517/518 빌드 설정 (v1.1.3)
└── setup.py                        # 레거시 빌드 지원 설정
```

---

## 3. 설치 및 프로비저닝 메커니즘 (`installer.py`)

프레임워크의 설치는 `termux_stt/platform/installer.py`의 `EngineInstaller` 클래스가 총괄합니다.

```
[termux-stt install]
         |
         v
1. install_system_dependencies()
   └─> pkg install -y ffmpeg libbluray libxml2 git termux-api curl
         |
         v
2. install_whisper_cpp()
   ├─> Step 2-1: _download_prebuilt_whisper() (우선순위 1)
   │   └─> GitHub Releases (v1.1.3 ~ v1.0.0) ARM64 Bionic 바이너리 고속 다운로드
   │       성공 시: ~/.local/bin/whisper-cli 및 $PREFIX/bin 복사 후 권한(0o755) 부여
   │
   └─> Step 2-2: Fallback Local Compilation (우선순위 2)
       ├─> pkg install -y cmake make clang
       ├─> git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git
       └─> cmake -B build -DBUILD_SHARED_LIBS=OFF -DWHISPER_NEON=ON -DCMAKE_BUILD_TYPE=Release
           cmake --build build -j(nproc)
         |
         v
3. install_vosk() & install_sherpa_onnx()
   └─> ~/.cache/termux-stt/models/ 디렉터리 구조 초기화
```

### 소스 코드 분석: `installer.py`

```python
class EngineInstaller:
    """Automated installer for native dependencies and C++ engines."""

    PREBUILT_WHISPER_URLS = [
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.3/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.2/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.1/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.0/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.0.0/whisper-cli-arm64-android",
    ]

    @classmethod
    def install_system_dependencies(cls) -> bool:
        """Termux 필수 런타임 패키지 설치"""
        if not shutil.which("pkg"):
            return True
        cmd = ["pkg", "install", "-y", "ffmpeg", "libbluray", "libxml2", "git", "termux-api", "curl"]
        res = subprocess.run(cmd, check=False)
        return res.returncode == 0

    @classmethod
    def _download_prebuilt_whisper(cls) -> bool:
        """사전 컴파일된 ARM64 Bionic 바이너리 고속 다운로드"""
        LOCAL_BIN.mkdir(parents=True, exist_ok=True)
        target_path = LOCAL_BIN / "whisper-cli"

        for url in cls.PREBUILT_WHISPER_URLS:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "termux-stt-installer/1.1.1 (Android; ARM64)"})
                with urllib.request.urlopen(req, timeout=10) as response, open(target_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

                # 파일 크기가 100KB 이상인 유효 실행 파일인지 확인
                if target_path.exists() and target_path.stat().st_size > 100 * 1024:
                    target_path.chmod(0o755)
                    shutil.copy2(target_path, LOCAL_BIN / "whisper-cpp")
                    (LOCAL_BIN / "whisper-cpp").chmod(0o755)
                    # 쓰기 가능한 경우 $PREFIX/bin 에도 동기화
                    if PREFIX_BIN.exists() and os.access(PREFIX_BIN, os.W_OK):
                        shutil.copy2(target_path, PREFIX_BIN / "whisper-cli")
                        shutil.copy2(target_path, PREFIX_BIN / "whisper-cpp")
                        (PREFIX_BIN / "whisper-cli").chmod(0o755)
                        (PREFIX_BIN / "whisper-cpp").chmod(0o755)
                    return True
            except Exception:
                continue
        return False
```

---

## 4. 플랫폼 적응 및 모바일 안전 계층 (`platform/`)

### 4.1 하드웨어 감지: `hardware.py`
- **SoC 및 코어 탐지**: `/proc/cpuinfo`의 `Hardware` 항목을 읽어 Qualcomm Snapdragon, Samsung Exynos, MediaTek Dimensity, Google Tensor 등을 식별합니다.
- **big.LITTLE 스레드 최적화**: 모바일 CPU는 고성능 빅코어(Big)와 저전력 리틀코어(Little)로 구성됩니다. 전체 코어를 모두 점유할 경우 스로틀링과 발열이 발생하므로 `get_optimal_threads()`는 전체 코어의 절반(주로 빅코어 개수)을 최적 스레드로 산출합니다.
- **NEON / FP16 지원 여부**: `neon`, `asimd`, `fphp`, `asimdhp` 플래그를 정규식으로 검증합니다.
- **Platform SSOT**: `is_termux()`는 `ameva-vulkan-runtime.platform`의 SSOT를 우선 참조하고 미설치 시 환경변수 `PREFIX` 검증으로 폴백합니다.

### 4.2 백그라운드 절전 방지: `mobile_guard.py`
Termux 환경에서 긴 시간 동안 전사 작업을 수행할 때 단말기가 절전 상태로 들어가지 않도록 `termux-wake-lock`을 획득하고, 작업 완료 또는 예외 발생 시 반드시 `termux-wake-unlock`을 호출하도록 RAII 패턴의 컨텍스트 매니저를 제공합니다:

```python
@contextmanager
def wake_lock():
    """RAII Context Manager guaranteeing termux-wake-unlock upon exit or error."""
    guard = MobileGuard()
    guard.acquire_wakelock()
    try:
        yield guard
    finally:
        guard.release_wakelock()
```

### 4.3 서브프로세스 샌드박스 격리: `process_pool.py`
`run_isolated(cmd, timeout, env, max_retries=2)` 함수는 외부 C++ 바이너리를 실행하며, 프로세스가 시그널(`returncode < 0`, 예: SIGSEGV -11)로 종료되거나 타임아웃이 발생할 경우 파이썬 메인 런타임의 크래시를 방지하고 설정된 횟수만큼 격리 재시도를 수행합니다.

---

## 5. 오디오 파이프라인 (`audio/`)

```
Input Audio File (.wav, .mp3, .m4a, .flac, .ogg, .opus, .webm)
         |
         v
1. validate_audio() [preprocessor.py] -> 파일 존재 및 헤더 크기(>44B) 검증
         |
         v
2. _check_pure_wav() [preprocessor.py]
   ├─> 순수 파이썬 wave 모듈로 확인: 16000Hz / Mono(1ch) / 16-bit PCM s16le 인가?
   │   ├─> [YES]: FFmpeg 변환 없이 그대로 반환 (0ms 지연, 무변환 패스스루)
   │   └─> [NO]: FFmpeg 실행
         |
         v
3. preprocess() [preprocessor.py]
   └─> ffmpeg -y -i <input> -ac 1 -ar 16000 -c:a pcm_s16le <output.wav>
       (Termux libbluray 동적 링커 에러 발생 시 pkg install libbluray libxml2 자동 복구)
         |
         v
4. detect_speech() / EnergyVAD [vad.py]
   └─> RMS 에너지 문턱값 기반 유효 발화 구간(Segments) 검출 및 무음 제거
```

### 오디오 모듈 주요 구현 특징
- `loader.py`: 파일 메타데이터 조회 시 순수 파이썬 `wave.open()`을 1차로 시도하여 서브프로세스 호출 오버헤드를 배제하고, MP3/M4A 등 비-WAV 파일에 한해 `ffprobe -print_format json`을 실행합니다.
- `preprocessor.py`: Termux 환경에서 FFmpeg 실행 시 빈번하게 발생하는 `libbluray.so` 누락 에러(`CalledProcessError`)를 포착하여 `pkg install -y libbluray libxml2`를 즉시 실행한 후 명령어를 재시도하는 자가 복구(Self-Healing) 로직을 갖추고 있습니다.
- `vad.py`: 표준 라이브러리 `struct.unpack("<{n}h", data)`를 통해 30ms 프레임 단위로 RMS(Root Mean Square) 음향 에너지를 계산하는 `EnergyVAD`를 제공합니다.

---

## 6. STT 엔진 추상화 계층 (`engine/`)

모든 백엔드는 `Engine` 추상 기본 클래스를 상속하며, 표준화된 5개 인터페이스를 제공합니다:

| 메서드 시그니처 | 반환 타입 | 기능 설명 |
| :--- | :--- | :--- |
| `transcribe(audio_path, **kwargs)` | `TranscriptResult` | 전체 오디오 파일 단일 전사 |
| `stream_mic(duration=None)` | `Iterator[Segment]` | 마이크 실시간 스트리밍 전사 |
| `stream_file(audio_path, chunk_sec=5.0)` | `Iterator[Segment]` | 대용량 파일 청크 단위 스트리밍 전사 |
| `diarize(audio_path, num_speakers=2)` | `DiarizedResult` | 발화 텍스트 + 화자 식별 레이블 분리 |
| `get_info()` | `Dict[str, Any]` | 엔진 상태, 모델명, 스레드, 가속 장치 메타데이터 |

### 6.1 WhisperEngine: `whisper_engine.py`
`whisper.cpp` 바이너리를 서브프로세스로 구동하는 엔진입니다.
- **바이너리 탐색 휴리스틱**: `PATH` 내 `whisper-cli`, `whisper-cpp`, `main` 확인 후 `$PREFIX/bin`, `~/.local/bin` 순으로 자동 탐색.
- **GPU 오프로드 감지 (`_supports_ngl`)**: 해당 바이너리가 Vulkan GPU 가속 플래그(`-ngl` 또는 `--gpu-layers`)를 지원하는지 바이너리 도움말(`-h`)을 검사하여 안전하게 옵션을 주입합니다.
- **출력 파싱 2단계 폴백**:
  1. `-oj` 플래그를 통해 생성되는 `<wav_path>.json`의 오프셋(`from`, `to`) 및 텍스트를 구조화 파싱.
  2. JSON 출력이 누락된 경우 stdout의 타임스탬프 패턴(`[00:01:10.000 --> 00:01:15.000]`)을 정규식으로 파싱.

### 6.2 VoskEngine: `vosk_engine.py`
Kaldi 기반 음성인식 라이브러리인 Vosk를 로드합니다.
- **`_spoof_platform()`**: 안드로이드 Termux 환경의 `sys.platform`이 `linux-android` 등으로 보고될 때 Vosk의 CFFI 로더가 공유 객체를 찾지 못하는 문제를 해결하기 위해 `sys.platform = 'linux'`로 스푸핑합니다.
- **X-Vector 추출 (`extract_xvectors`)**: `vosk.SpkModel`을 연동하여 2.0초 청크 단위로 128차원 부동소수점 임베딩 벡터를 추출합니다.

### 6.3 SherpaEngine: `sherpa_engine.py`
차세대 Kaldi 프로젝트인 `sherpa-onnx`를 서브프로세스로 구동합니다.
`tokens.txt`, `encoder.onnx`, `decoder.onnx`, `joiner.onnx` 모델 파라미터를 결합하여 Zipformer 모델 전사를 실행합니다.

---

## 7. 하이브리드 화자 분리 파이프라인 (`engine/hybrid_engine.py`)

`termux-stt`의 핵심 아키텍처인 **Hybrid Pipeline**은 단말기 메모리 1.5GB 미만에서 고정밀 음성인식과 화자 분리를 동시에 수행합니다.

```
                         [ Audio Input File ]
                                  |
                                  v
                        Preprocess (16kHz Mono)
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
 [ Vosk Engine (SpkModel) ]                  [ Whisper.cpp Engine ]
  - 128-d X-Vector per 2.0s                   - High-accuracy ASR
  - Ultra-lightweight (220MB RAM)             - Produces Segments with
            |                                   precise start/end timestamps
            v                                           |
 [ Pure-Python KMeans ]                                 |
  - n_clusters = num_speakers                           |
  - Cluster Labels (0, 1, ...)                          |
            |                                           |
            +---------------------+---------------------+
                                  |
                                  v
                   [ SpeakerMapper.align() ]
                    - Time overlap window matching
                    - Pause gap (>1.2s) turn-taking heuristic
                                  |
                                  v
                        [ DiarizedResult ]
                 Segment(text="...", speaker="Speaker_0")
                 Segment(text="...", speaker="Speaker_1")
```

### 소스 코드 분석: `hybrid_engine.py`

```python
def diarize(self, audio_path: str, num_speakers: int = 2) -> DiarizedResult:
    # 1. 16kHz 모노 전처리
    wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
    is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

    try:
        # 2. Vosk X-Vector 128차원 임베딩 추출 (2.0초 청크 단위)
        try:
            xvectors = self._vosk.extract_xvectors(wav_path, chunk_sec=2.0)
        except Exception as exc:
            logger.warning("X-Vector extraction failed: %s — falling back", exc)
            xvectors = []

        # 3. 순수 파이썬 K-Means 클러스터링
        speaker_labels = []
        if xvectors and len(xvectors) >= num_speakers:
            vectors = [xv[2] for xv in xvectors]
            kmeans = KMeans(n_clusters=num_speakers)
            kmeans.fit(vectors)

            speaker_labels = [
                (xv[0], xv[1], label)
                for xv, label in zip(xvectors, kmeans.labels_)
            ]
        elif xvectors:
            speaker_labels = [(xv[0], xv[1], i % num_speakers) for i, xv in enumerate(xvectors)]

        # 4. Whisper.cpp 고정밀 텍스트 전사
        stt_result = self._whisper.transcribe(wav_path)

        # 5. 시간 오버랩 기반 텍스트 세그먼트와 화자 클러스터 정렬
        mapper = SpeakerMapper()
        aligned = mapper.align(stt_result.segments, speaker_labels)

        # 6. 화자 분리 결과 반환
        unique_speakers = sorted(set(s.speaker for s in aligned if s.speaker))
        return DiarizedResult(
            text=" ".join(s.text for s in aligned),
            language=stt_result.language,
            segments=aligned,
            duration=stt_result.duration,
            speakers=unique_speakers,
        )
    finally:
        if is_temp_wav and os.path.exists(wav_path):
            os.remove(wav_path)
```

---

## 8. 화자 분리 알고리즘 계층 (`diarization/`)

### 8.1 의존성 없는 순수 파이썬 K-Means: `clustering.py`
모바일 환경에서는 `scikit-learn`의 설치 용량(수백 MB) 및 C-컴파일러 문제가 심각합니다. 이를 위해 벡터 거리 계산과 K-Means 클러스터링 알고리즘을 표준 라이브러리 `math`와 `random`만으로 구현했습니다.

- **유클리드 거리**: $\sqrt{\sum (a_i - b_i)^2}$
- **코사인 유사도**: $\frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \|\mathbf{b}\|}$
- **KMeans 수렴 조건**: 중심점(Centroid) 이동 거리 합이 `tolerance`(1e-4) 미만이 되거나 `max_iter`(100회) 도달 시 반복 종료.

### 8.2 화자-세그먼트 정렬: `mapper.py`
Whisper의 발화 구간 `[seg.start, seg.end]`와 Vosk X-Vector 구간 `[spk.start, spk.end]`의 겹치는 시간 길이(Overlap Duration)를 계산하여 가장 큰 오버랩을 가지는 화자 클러스터를 발화자(`Speaker_0`, `Speaker_1` 등)로 매핑합니다.
만약 X-Vector 추출이 불가능한 경우 발화 간 침묵 공백(Pause Gap)이 1.2초를 초과할 때 발화자가 전환되는 턴테이킹(Turn-taking) 휴리스틱으로 안전하게 전환됩니다.

---

## 9. 모델 레지스트리 및 허브 (`models/`)

### 9.1 모델 레지스트리: `registry.py`
Whisper GGML 모델군, Vosk 음향 모델, Sherpa-ONNX 모델의 다운로드 URL, 파일 크기, 해시 정보를 중앙 관리합니다:
- **Whisper**: `tiny` (75MB), `base` (142MB), `small` (466MB), `small-q5_1` (182MB), `medium` (1.5GB), `large-v3-turbo` (1.6GB), `large-v3-turbo-q5_0` (560MB)
- **Vosk**: `small-ko-0.22` (42MB), `model-spk-0.4` (13MB)

### 9.2 모델 다운로드 허브: `hub.py`
- **경로 우선순위**: 지정한 모델명이 로컬에 존재하는 실제 파일 경로일 경우 다운로드를 생략하고 절대 경로로 즉시 반환합니다.
- **SSL 핸드셰이크 복구**: 안드로이드 Termux 환경의 시스템 CA 인증서 누락에 대응하기 위해 표준 SSL 컨텍스트 실패 시 unverified 컨텍스트로 복구 재시도합니다.
- **오타 교정 제안**: 레지스트리에 없는 모델명을 입력할 경우 `difflib.get_close_matches`를 구동하여 유사 모델명을 사용자에게 제안합니다.

### 9.3 양자화 선택기: `quantization.py`
가용 RAM 크기에 따른 권장 양자화 레벨:
- 가용 RAM > 4GB: `f16`
- 2GB ~ 4GB: `q8_0`
- 1GB ~ 2GB: `q5_1`
- 1GB 미만: `q4_0`

---

## 10. 내보내기 포맷 계층 (`export/`)

### 10.1 데이터 모델: `result.py`
```python
@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None

@dataclass
class TranscriptResult:
    text: str
    segments: List[Segment]
    language: Optional[str] = None
    duration: Optional[float] = None
```

### 10.2 지원 포맷 및 구현
- `srt.py`: `00:00:01,250 --> 00:00:04,500` 형식의 표준 SubRip 자막 파일 생성. 화자 정보가 있을 경우 `[Speaker_0] 내용` 형태로 인라인 표기.
- `vtt.py`: `WEBVTT` 헤더 및 마침표(`.`) 밀리초 포맷 변환.
- `json_export.py`: `asdict(result)` 기반 UTF-8 JSON 직렬화.
- `rttm.py`: NIST Rich Transcription 화자 분리 표준 포맷 (`SPEAKER file 1 <start> <duration> <NA> <NA> <speaker> <NA> <NA>`).

---

## 11. CLI 실행 체계 (`cli/`)

### 11.1 서브커맨드 목록
1. `termux-stt install`: 의존성 패키지 및 `whisper.cpp` 네이티브 런타임 1-Click 자동 설치.
2. `termux-stt transcribe <file>`: 오디오 파일 전사 (텍스트, JSON, SRT, VTT 출력).
3. `termux-stt diarize <file> --speakers <N>`: 하이브리드 화자 분리 및 전사 (RTTM, JSON, Text 출력).
4. `termux-stt listen --duration <sec>`: 실시간 마이크 입력 스트리밍 전사.
5. `termux-stt doctor`: OS, FFmpeg, Python 버전, 네이티브 엔진 바이너리 상태 종합 진단.
6. `termux-stt benchmark --audio <file>`: RTF(Real Time Factor) 및 메모리 소비량 측정.
7. `termux-stt models <list|download|remove>`: 로컬 모델 캐시 관리.

### 11.2 안드로이드 읽기 전용 `/tmp` 자동 우회 로직
사용자가 `--output /tmp/output.srt` 와 같이 리눅스 관행 경로를 입력했을 때 안드로이드 권한 에러를 차단하는 로직입니다:
```python
def resolve_safe_output_path(path: str) -> str:
    if not path:
        return path
    p = Path(path)
    if str(p).startswith("/tmp") and not os.access("/tmp", os.W_OK):
        fallback_dir = os.environ.get("TMPDIR") or os.path.expanduser("~/tmp") or "."
        os.makedirs(fallback_dir, exist_ok=True)
        safe_path = os.path.join(fallback_dir, p.name)
        print(f"[*] Notice: Root '/tmp' is read-only on Android. Safe redirected output to: '{safe_path}'")
        return safe_path
    return path
```

---

## 12. Node.js 연동 레이어 (`lib/`, `bin/`)

NPM 생태계(`npx termux-stt` 또는 Node.js 백엔드) 연동을 지원합니다.
- `bin/termux-stt.js`: `python3` 또는 `python` 실행 바이너리를 자동 감지하여 `python -m termux_stt.cli.main`으로 CLI 인수를 투명하게 포워딩합니다.
- `lib/engine.js`: JavaScript `TranscriptResult`, `Segment` 및 시간 포맷터(`formatTime`) 제공.
- `lib/whisper.js`, `lib/hybrid.js`: `child_process.spawn`을 통해 파이썬 CLI를 비동기 호출하고 JSON 결과를 프로미스(`Promise<TranscriptResult>`)로 반환합니다.

---

## 13. 엔드투엔드 실행 가이드 (설치부터 전 기능 사용법)

### 단계 1: 환경 설치 (Installation)
Termux 콘솔에서 다음 단일 명령을 실행합니다:
```bash
# pip를 통한 패키지 설치
pip install termux-stt

# 1-Click 네이티브 런타임 및 FFmpeg 자동 프로비저닝
termux-stt install
```

시스템 환경이 정상적으로 구성되었는지 진단합니다:
```bash
termux-stt doctor
```

### 단계 2: 기본 음성 전사 (Basic Transcription)
```bash
# 기본 whisper 베이스 모델로 한국어 전사
termux-stt transcribe meeting.m4a --lang ko

# SRT 자막 파일 생성
termux-stt transcribe interview.wav --format srt --output interview.srt

# 가용 RAM이 적은 환경: 5비트 양자화 모델 및 스레드 4개 지정
termux-stt transcribe audio.mp3 --quantization q5_1 --threads 4
```

### 단계 3: 화자 분리 전사 (Speaker Diarization)
```bash
# 2인 대화 파일 화자 분리
termux-stt diarize debate.wav --speakers 2

# RTTM 표준 화자 분리 파일로 저장
termux-stt diarize meeting.wav --speakers 3 --format rttm --output meeting.rttm
```

### 단계 4: 마이크 실시간 청취 (Real-time Listening)
```bash
# 30초 동안 마이크 입력 실시간 전사
termux-stt listen --duration 30 --lang ko
```

### 단계 5: 파이썬 API 연동 (Python SDK)
```python
import termux_stt

# 1. 고정밀 Whisper 엔진 생성
engine = termux_stt.create_engine(
    engine="whisper",
    model="base",
    lang="ko",
    threads=4
)
result = engine.transcribe("speech.wav")
print("전체 전사:", result.text)
for seg in result.segments:
    print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")

# 2. 하이브리드 화자 분리 엔진 생성
hybrid = termux_stt.create_engine(
    engine="hybrid",
    model="base",
    lang="ko",
    num_speakers=2
)
diar_result = hybrid.diarize("interview.wav", num_speakers=2)
for seg in diar_result.segments:
    print(f"[{seg.speaker}] {seg.text}")
```

### 단계 6: 성능 벤치마크 실행 (Benchmarking)
```bash
termux-stt benchmark --audio test_10s.wav --engine whisper
```
출력 결과로 실시간 계수(RTF: Real Time Factor)와 피크 메모리 사용량(MB)이 산출됩니다. RTF가 1.0 미만일 경우 오디오 재생 시간보다 빠르게 전사가 완료됨을 의미합니다.

---

## 14. 요약 및 기술적 결론

`termux-stt`는 안드로이드 Termux 환경의 플랫폼적 한계(OOM, 절전 모드, C-컴파일 복잡도, 플랫폼 감지 결함)를 다음과 같이 해결했습니다:
1. **격리성**: 서브프로세스 샌드박스로 C++ 런타임 크래시 전파 차단.
2. **경량성**: Pure-Python K-Means 및 Pure-Python wave 헤더 선행 파싱으로 C 확장 모듈 메모리 부담 배제.
3. **효율성**: Vosk 128차원 X-Vector와 Whisper.cpp 음성인식을 결합한 하이브리드 파이프라인을 통해 모바일 RAM 1.5GB 미만에서 화자 분리 완결.
4. **안정성**: RAII `wake_lock`, `/tmp` 자동 우회, FFmpeg 라이브러리 자동 복구로 무인 자동화 환경 보장.
