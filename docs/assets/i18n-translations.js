/**
 * AMEVA Ecosystem - Multilingual Translation Dictionary (6 Languages)
 * English (en), Korean (ko), Japanese (ja), Chinese (zh), Spanish (es), Hindi (hi)
 * Aligned with AMEVA Library Documentation Template System
 */

(function(global) {
  'use strict';

  const translations = {
    en: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (Unified STT)",
        pypiBtn: "PyPI (Python)",
        npmBtn: "npm (Node.js)",
        githubBtn: "GitHub",
        footerText: "© 2026 termux-stt Project (uno-km). Released under the MIT License.",
        nav: {
          overview: "Overview",
          home: "Home / Architecture",
          installation: "Installation Guide",
          quickstart: "Quickstart & Recipes",
          models: "Model Hub & Registry",
          advancedParams: "Advanced Parameters",
          apiReference: "100% Full API Reference",
          benchmarks: "Benchmarks & Hardware",
          versions: "Version Archive"
        }
      },
      home: {
        title: "Android On-Device Unified STT Framework",
        subtitle: "Whisper.cpp, Vosk, and Sherpa-ONNX unified with Speaker Diarization and 0 external ML dependencies on Termux.",
        quickInstall: "Quick Install",
        features: {
          f1Title: "Multi-Engine Abstraction",
          f1Desc: "Unified create_engine() API for whisper.cpp, vosk, and sherpa-onnx.",
          f2Title: "Pure-Python Diarization",
          f2Desc: "Cosine similarity & K-Means clustering in pure Python. Zero numpy/sklearn dependencies.",
          f3Title: "Hybrid Pipeline",
          f3Desc: "Vosk 128d X-Vector + Whisper STT under 1.5 GB RAM on mobile devices.",
          f4Title: "Subprocess Isolation",
          f4Desc: "C++ engines isolated in subprocesses. Host Python runtime never crashes on Segfault.",
          f5Title: "Mobile Resilient",
          f5Desc: "Built-in WakeLock, Doze mode bypass, and Android memory safeguards.",
          f6Title: "Dual-Engine Ecosystem",
          f6Desc: "First-class Python (pip) and Node.js (npm) packages with identical APIs."
        }
      },
      installation: {
        title: "Installation Guide",
        subtitle: "Setup termux-stt in Android Termux environment with zero compilation headaches.",
        prereqTitle: "Prerequisites in Termux",
        pkgTitle: "Package Installation",
        androidTweaksTitle: "Android Environment Tweaks (Recommended)",
        verifyTitle: "Verification"
      },
      quickstart: {
        title: "Quickstart & Recipes",
        subtitle: "Production-ready code snippets for common audio transcription workflows.",
        r1Title: "Recipe 1: Simple File Transcription",
        r2Title: "Recipe 2: Realtime Microphone Streaming",
        r3Title: "Recipe 3: Speaker Diarization (Meeting Minutes)",
        r4Title: "Recipe 4: Batch Processing Directory"
      },
      models: {
        title: "Model Hub & Registry",
        subtitle: "Curated lightweight on-device models with automatic downloading and SHA-256 integrity checks.",
        whisperTitle: "Whisper Models (GGML Quantized)",
        voskTitle: "Vosk Models (X-Vector & STT)",
        sherpaTitle: "Sherpa-ONNX Models",
        cliTitle: "CLI Model Management"
      },
      advancedParams: {
        title: "Advanced Parameters Handbook",
        subtitle: "Fine-tune inference speed, memory footprint, VAD sensitivity, and clustering accuracy.",
        vadTitle: "1. VAD & Silence Thresholds",
        threadTitle: "2. CPU Thread Optimization",
        quantTitle: "3. Quantization Levels",
        clusterTitle: "4. Diarization & Clustering"
      },
      apiReference: {
        title: "100% Full API Reference",
        subtitle: "Complete specification for Python SDK, Node.js SDK, and CLI commands.",
        pythonTitle: "Python SDK (termux_stt)",
        nodeTitle: "Node.js SDK (termux-stt)",
        cliTitle: "CLI Commands"
      },
      benchmarks: {
        title: "Empirical Benchmarks & Hardware",
        subtitle: "Measured on Samsung Galaxy A35 5G (Exynos 1380, 6GB RAM, Android 14 Termux).",
        specTitle: "Test Hardware Environment",
        matrixTitle: "Empirical Benchmark Matrix",
        findingsTitle: "Key Empirical Findings"
      },
      versions: {
        title: "Version Archive & Release Notes",
        subtitle: "Release history and upgrade guides for termux-stt.",
        v100Title: "v1.0.0 (Initial Public Release) - 2026-08-20"
      }
    },
    ko: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (통합 STT)",
        pypiBtn: "PyPI (파이썬)",
        npmBtn: "npm (Node.js)",
        githubBtn: "깃허브",
        footerText: "© 2026 termux-stt 프로젝트 (uno-km). MIT 라이선스.",
        nav: {
          overview: "개요",
          home: "홈 / 아키텍처",
          installation: "설치 가이드",
          quickstart: "퀵스타트 & 레시피",
          models: "모델 허브 & 레지스트리",
          advancedParams: "고급 제어 파라미터",
          apiReference: "100% 전체 API 명세",
          benchmarks: "벤치마크 & 하드웨어",
          versions: "버전 아카이브"
        }
      },
      home: {
        title: "안드로이드 온디바이스 통합 음성인식(STT) 프레임워크",
        subtitle: "Whisper.cpp, Vosk, Sherpa-ONNX를 단 3줄로 통합. 화자 분리 내장, 순수 Python 수학 연산으로 외부 ML 의존성 0개.",
        quickInstall: "원터치 빠른 설치",
        features: {
          f1Title: "멀티 엔진 단일 추상화",
          f1Desc: "whisper.cpp, vosk, sherpa-onnx를 create_engine() 단일 함수로 제어.",
          f2Title: "순수 Python 화자 분리",
          f2Desc: "외부 numpy/sklearn 없이 순수 Python으로 코사인 유사도 및 K-Means 클러스터링 구현.",
          f3Title: "하이브리드 파이프라인",
          f3Desc: "Vosk 128차원 X-Vector 화자 지문 + Whisper STT를 1.5GB 이하 RAM으로 구동.",
          f4Title: "프로세스 격리 안정성",
          f4Desc: "C++ 엔진을 서브프로세스로 격리하여 Segfault 발생 시에도 파이썬 프로세스 안전 생존.",
          f5Title: "모바일 생존성 강화",
          f5Desc: "WakeLock 자동 획득, Doze 모드 우회 및 Phantom Process 방어 내장.",
          f6Title: "Python & Node.js 듀얼 지원",
          f6Desc: "PyPI 및 npm 생태계 모두에서 완벽히 동일한 API와 CLI 제공."
        }
      },
      installation: {
        title: "설치 가이드",
        subtitle: "컴파일 오류 없이 안드로이드 Termux 환경에 원클릭으로 termux-stt를 구축합니다.",
        prereqTitle: "Termux 사전 요구사항",
        pkgTitle: "패키지 설치",
        androidTweaksTitle: "안드로이드 환경 최적화 (권장)",
        verifyTitle: "설치 검증"
      },
      quickstart: {
        title: "퀵스타트 & 실전 레시피",
        subtitle: "파일 전사, 실시간 마이크 스트리밍, 화자 분리를 위한 실전 코드 스니펫.",
        r1Title: "레시피 1: 단일 오디오 파일 전사",
        r2Title: "레시피 2: 실시간 마이크 스트리밍 자막",
        r3Title: "레시피 3: 화자 분리 회의록 자동 생성",
        r4Title: "레시피 4: 디렉터리 일괄 배치 처리"
      },
      models: {
        title: "모델 허브 & 레지스트리",
        subtitle: "SHA-256 무결성 검증 및 자동 다운로드가 지원되는 온디바이스 경량 모델 컬렉션.",
        whisperTitle: "Whisper 모델 (GGML 양자화)",
        voskTitle: "Vosk 모델 (X-Vector & STT)",
        sherpaTitle: "Sherpa-ONNX 모델",
        cliTitle: "CLI 모델 관리 명령어"
      },
      advancedParams: {
        title: "고급 제어 파라미터 핸드북",
        subtitle: "추론 속도, 메모리 점유율, VAD 감도, 클러스터링 정밀도 미세 튜닝 가이드.",
        vadTitle: "1. VAD 및 무음 필터링 임계값",
        threadTitle: "2. CPU 스레드 최적화",
        quantTitle: "3. 양자화 레벨 선택",
        clusterTitle: "4. 화자 분리 클러스터링 인자"
      },
      apiReference: {
        title: "100% 전체 API 명세",
        subtitle: "Python SDK, Node.js SDK, CLI 명령어의 완벽한 함수 시그니처 및 옵션 명세.",
        pythonTitle: "Python SDK (termux_stt)",
        nodeTitle: "Node.js SDK (termux-stt)",
        cliTitle: "CLI 명령어"
      },
      benchmarks: {
        title: "실측 벤치마크 & 하드웨어 프로파일링",
        subtitle: "삼성 갤럭시 A35 5G (Exynos 1380, 6GB RAM, 안드로이드 14 Termux) 실측 데이터.",
        specTitle: "테스트 하드웨어 환경",
        matrixTitle: "실측 벤치마크 매트릭스",
        findingsTitle: "핵심 실증 발견점"
      },
      versions: {
        title: "버전 아카이브 & 릴리즈 노트",
        subtitle: "termux-stt 프레임워크의 변경 이력 및 업그레이드 가이드.",
        v100Title: "v1.0.0 (공식 첫 릴리즈) - 2026-08-20"
      }
    },
    ja: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (統合STT)",
        pypiBtn: "PyPI (Python)",
        npmBtn: "npm (Node.js)",
        githubBtn: "GitHub",
        footerText: "© 2026 termux-stt プロジェクト (uno-km). MITライセンス.",
        nav: {
          overview: "概要",
          home: "ホーム / アーキテクチャ",
          installation: "インストールガイド",
          quickstart: "クイックスタート",
          models: "モデルハブ",
          advancedParams: "詳細パラメータ",
          apiReference: "完全APIリファレンス",
          benchmarks: "ベンチマーク",
          versions: "バージョン履歴"
        }
      },
      home: {
        title: "Android オンデバイス統合音声認識 (STT) フレームワーク",
        subtitle: "Whisper.cpp、Vosk、Sherpa-ONNXを統合。話者分離内蔵、外部ML依存性ゼロ。",
        quickInstall: "クイックインストール",
        features: {
          f1Title: "マルチエンジン統合",
          f1Desc: "1つのAPIでwhisper.cpp、vosk、sherpa-onnxを透過的に制御。",
          f2Title: "純Python話者分離",
          f2Desc: "numpyやsklearn不要。純粋なPythonでK-Meansとコサイン類似度を実装。",
          f3Title: "ハイブリッド構成",
          f3Desc: "Vosk X-Vector + Whisper STTでメモリ1.5GB以下の高精度話者分離。",
          f4Title: "プロセス分離",
          f4Desc: "C++エンジンをサブプロセスで隔離し、クラッシュを防止。",
          f5Title: "モバイル最適化",
          f5Desc: "WakeLockとDozeモード回避を内蔵し、バックグラウンド処理を保護。",
          f6Title: "デュアルエコシステム",
          f6Desc: "PythonとNode.jsの両方で同一の使い勝手を提供。"
        }
      },
      installation: {
        title: "インストールガイド",
        subtitle: "コンパイルの煩わしさなく、Android Termuxにワンクリックでtermux-sttを導入。",
        prereqTitle: "Termux の事前要件",
        pkgTitle: "パッケージインストール",
        androidTweaksTitle: "Android環境の最適化 (推奨)",
        verifyTitle: "インストールの検証"
      },
      quickstart: {
        title: "クイックスタート & 実践レシピ",
        subtitle: "ファイル文字起こし、リアルタイムマイク、話者分離のためのコードスニペット。",
        r1Title: "レシピ 1: 単一音声ファイルの文字起こし",
        r2Title: "レシピ 2: リアルタイムマイク字幕生成",
        r3Title: "レシピ 3: 話者分離議事録生成",
        r4Title: "レシピ 4: ディレクトリの一括バッチ処理"
      },
      models: {
        title: "モデルハブ & レジストリ",
        subtitle: "SHA-256整合性チェックと自動ダウンロードを備えたオンデバイス軽量モデル一覧。",
        whisperTitle: "Whisper モデル (GGML量子化)",
        voskTitle: "Vosk モデル (X-Vector & STT)",
        sherpaTitle: "Sherpa-ONNX モデル",
        cliTitle: "CLIモデル管理コマンド"
      },
      advancedParams: {
        title: "詳細パラメータハンドブック",
        subtitle: "推論速度、メモリ使用量、VAD感度、クラスタリング精度の微調整ガイド。",
        vadTitle: "1. VAD と無音しきい値",
        threadTitle: "2. CPUスレッド最適化",
        quantTitle: "3. 量子化レベルの選択",
        clusterTitle: "4. 話者分離クラスタリング設定"
      },
      apiReference: {
        title: "100% 完全 API リファレンス",
        subtitle: "Python SDK、Node.js SDK、CLIコマンドの詳細な仕様一覧。",
        pythonTitle: "Python SDK (termux_stt)",
        nodeTitle: "Node.js SDK (termux-stt)",
        cliTitle: "CLI コマンド"
      },
      benchmarks: {
        title: "実測ベンチマーク & ハードウェア情報",
        subtitle: "Samsung Galaxy A35 5G (Exynos 1380, 6GB RAM, Android 14) 上での実測データ。",
        specTitle: "テストハードウェア環境",
        matrixTitle: "実測ベンチマークマトリクス",
        findingsTitle: "主な実証的知見"
      },
      versions: {
        title: "バージョンアーカイブ & リリースノート",
        subtitle: "termux-sttフレームワークの更新履歴とアップグレードガイド。",
        v100Title: "v1.0.0 (初回公開リリース) - 2026-08-20"
      }
    },
    zh: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (统一STT)",
        pypiBtn: "PyPI (Python)",
        npmBtn: "npm (Node.js)",
        githubBtn: "GitHub",
        footerText: "© 2026 termux-stt 项目 (uno-km)。基于 MIT 许可证发布。",
        nav: {
          overview: "概览",
          home: "主页 / 架构",
          installation: "安装指南",
          quickstart: "快速入门",
          models: "模型中心",
          advancedParams: "高级参数",
          apiReference: "完整 API 参考",
          benchmarks: "性能基准",
          versions: "版本归档"
        }
      },
      home: {
        title: "Android 端侧统一语音识别 (STT) 框架",
        subtitle: "整合 Whisper.cpp、Vosk 与 Sherpa-ONNX，内置说话人分离，零外部机器学习依赖。",
        quickInstall: "一键快速安装",
        features: {
          f1Title: "多引擎统一抽象",
          f1Desc: "通过统一的 create_engine() 接口控制三大引擎。",
          f2Title: "纯 Python 说话人分离",
          f2Desc: "无需 numpy/sklearn，纯 Python 实现余弦相似度与 K-Means 聚类。",
          f3Title: "混合流水线",
          f3Desc: "Vosk X-Vector + Whisper STT，在移动设备上仅需不到 1.5GB 内存。",
          f4Title: "子进程故障隔离",
          f4Desc: "C++ 引擎运行于独立子进程，防止段错误影响主进程。",
          f5Title: "移动端保活优化",
          f5Desc: "内置 WakeLock 与 Doze 模式绕过机制。",
          f6Title: "双引擎生态",
          f6Desc: "同时提供 Python (pip) 与 Node.js (npm) 支持。"
        }
      },
      installation: {
        title: "安装指南",
        subtitle: "零编译烦恼，一键在 Android Termux 中部署 termux-stt。",
        prereqTitle: "Termux 前置要求",
        pkgTitle: "安装包配置",
        androidTweaksTitle: "Android 环境优化 (推荐)",
        verifyTitle: "安装验证"
      },
      quickstart: {
        title: "快速入门与实战配方",
        subtitle: "用于文件转录、实时麦克风与说话人分离的生产级代码片段。",
        r1Title: "配方 1: 单音频文件转录",
        r2Title: "配方 2: 实时麦克风流式字幕",
        r3Title: "配方 3: 说话人分离会议纪要",
        r4Title: "配方 4: 目录批量处理"
      },
      models: {
        title: "模型中心与注册表",
        subtitle: "支持 SHA-256 完整性校验与自动下载的端侧轻量级模型库。",
        whisperTitle: "Whisper 模型 (GGML 量化)",
        voskTitle: "Vosk 模型 (X-Vector & STT)",
        sherpaTitle: "Sherpa-ONNX 模型",
        cliTitle: "CLI 模型管理命令"
      },
      advancedParams: {
        title: "高级参数手册",
        subtitle: "微调推理速度、内存占用、VAD 灵敏度与聚类精度。",
        vadTitle: "1. VAD 与静音阈值",
        threadTitle: "2. CPU 线程优化",
        quantTitle: "3. 量化等级选择",
        clusterTitle: "4. 说话人分离聚类参数"
      },
      apiReference: {
        title: "100% 完整 API 参考",
        subtitle: "Python SDK、Node.js SDK 及 CLI 命令的完整规范。",
        pythonTitle: "Python SDK (termux_stt)",
        nodeTitle: "Node.js SDK (termux-stt)",
        cliTitle: "CLI 命令"
      },
      benchmarks: {
        title: "实测基准与硬件性能",
        subtitle: "在三星 Galaxy A35 5G (Exynos 1380, 6GB 内存, Android 14) 上的实测数据。",
        specTitle: "测试硬件环境",
        matrixTitle: "实测性能基准矩阵",
        findingsTitle: "关键实证发现"
      },
      versions: {
        title: "版本归档与发布说明",
        subtitle: "termux-stt 框架的历史版本与升级指南。",
        v100Title: "v1.0.0 (正式公开发布) - 2026-08-20"
      }
    },
    es: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (STT Unificado)",
        pypiBtn: "PyPI (Python)",
        npmBtn: "npm (Node.js)",
        githubBtn: "GitHub",
        footerText: "© 2026 Proyecto termux-stt (uno-km). Publicado bajo la Licencia MIT.",
        nav: {
          overview: "Resumen",
          home: "Inicio / Arquitectura",
          installation: "Guía de Instalación",
          quickstart: "Inicio Rápido",
          models: "Centro de Modelos",
          advancedParams: "Parámetros Avanzados",
          apiReference: "Referencia API Completa",
          benchmarks: "Pruebas de Rendimiento",
          versions: "Archivo de Versiones"
        }
      },
      home: {
        title: "Framework Unificado de Reconocimiento de Voz para Android",
        subtitle: "Whisper.cpp, Vosk y Sherpa-ONNX unificados con diarización de hablantes y cero dependencias de ML.",
        quickInstall: "Instalación Rápida",
        features: {
          f1Title: "Abstracción Multi-Motor",
          f1Desc: "Interfaz unificada create_engine() para los tres motores STT.",
          f2Title: "Diarización en Python Puro",
          f2Desc: "Similitud de coseno y K-Means sin numpy ni sklearn.",
          f3Title: "Pipeline Híbrido",
          f3Desc: "Vosk X-Vector + Whisper STT con menos de 1.5 GB de RAM.",
          f4Title: "Aislamiento de Procesos",
          f4Desc: "Motores C++ en subprocesos para evitar caídas de la aplicación.",
          f5Title: "Protección Móvil",
          f5Desc: "WakeLock integrado y evasión del modo Doze.",
          f6Title: "Ecosistema Dual",
          f6Desc: "Paquetes oficiales en Python y Node.js con APIs idénticas."
        }
      },
      installation: {
        title: "Guía de Instalación",
        subtitle: "Configure termux-stt en Android Termux sin dolores de cabeza de compilación.",
        prereqTitle: "Requisitos Previos en Termux",
        pkgTitle: "Instalación del Paquete",
        androidTweaksTitle: "Ajustes del Entorno Android (Recomendado)",
        verifyTitle: "Verificación"
      },
      quickstart: {
        title: "Inicio Rápido y Recetas",
        subtitle: "Fragmentos de código listos para producción para transcripción de audio.",
        r1Title: "Receta 1: Transcripción Simple de Archivo",
        r2Title: "Receta 2: Subtitulado en Tiempo Real con Micrófono",
        r3Title: "Receta 3: Diarización de Hablantes (Actas de Reuniones)",
        r4Title: "Receta 4: Procesamiento por Lotes de Directorios"
      },
      models: {
        title: "Centro de Modelos y Registro",
        subtitle: "Colección de modelos ligeros para el dispositivo con verificación SHA-256.",
        whisperTitle: "Modelos Whisper (Cuantizados en GGML)",
        voskTitle: "Modelos Vosk (X-Vector y STT)",
        sherpaTitle: "Modelos Sherpa-ONNX",
        cliTitle: "Comandos CLI de Gestión de Modelos"
      },
      advancedParams: {
        title: "Manual de Parámetros Avanzados",
        subtitle: "Ajuste fino de velocidad de inferencia, memoria, sensibilidad VAD y precisión de clustering.",
        vadTitle: "1. Umbrales VAD y de Silencio",
        threadTitle: "2. Optimización de Hilos de CPU",
        quantTitle: "3. Niveles de Cuantización",
        clusterTitle: "4. Parámetros de Diarización"
      },
      apiReference: {
        title: "Referencia API 100% Completa",
        subtitle: "Especificación completa para SDK de Python, SDK de Node.js y comandos CLI.",
        pythonTitle: "SDK de Python (termux_stt)",
        nodeTitle: "SDK de Node.js (termux-stt)",
        cliTitle: "Comandos CLI"
      },
      benchmarks: {
        title: "Pruebas de Rendimiento y Hardware",
        subtitle: "Medido en Samsung Galaxy A35 5G (Exynos 1380, 6GB RAM, Android 14 Termux).",
        specTitle: "Entorno de Hardware de Prueba",
        matrixTitle: "Matriz de Rendimiento Empírico",
        findingsTitle: "Hallazgos Clave"
      },
      versions: {
        title: "Archivo de Versiones y Notas de Lanzamiento",
        subtitle: "Historial de versiones y guías de actualización para termux-stt.",
        v100Title: "v1.0.0 (Lanzamiento Público Inicial) - 2026-08-20"
      }
    },
    hi: {
      common: {
        brand: "termux-stt",
        releaseTag: "v1.0.0 (एकीकृत STT)",
        pypiBtn: "PyPI (Python)",
        npmBtn: "npm (Node.js)",
        githubBtn: "GitHub",
        footerText: "© 2026 termux-stt परियोजना (uno-km). MIT लाइसेंस के तहत जारी।",
        nav: {
          overview: "अवलोकन",
          home: "होम / आर्किटेक्चर",
          installation: "स्थापना निर्देशिका",
          quickstart: "त्वरित शुरुआत",
          models: "मॉडल हब",
          advancedParams: "उन्नत पैरामीटर",
          apiReference: "पूर्ण API संदर्भ",
          benchmarks: "बेंचमार्क",
          versions: "संस्करण पुरालेख"
        }
      },
      home: {
        title: "एंड्रॉइड ऑन-डिवाइस एकीकृत वॉयस रिकग्निशन (STT) फ्रेमवर्क",
        subtitle: "Whisper.cpp, Vosk, और Sherpa-ONNX का एकीकरण। स्पीकर डायराइजेशन और शून्य बाहरी एमएल निर्भरता।",
        quickInstall: "त्वरित स्थापना",
        features: {
          f1Title: "मल्टी-इंजन अमूर्तता",
          f1Desc: "तीन इंजनों के लिए एकीकृत create_engine() इंटरफ़ेस।",
          f2Title: "प्योर पायथन डायराइजेशन",
          f2Desc: "बिना numpy/sklearn के कोसाइन समानता और K-Means क्लस्टरिंग।",
          f3Title: "हाइब्रिड पाइपलाइन",
          f3Desc: "Vosk X-Vector + Whisper STT 1.5 GB से कम रैम में।",
          f4Title: "प्रक्रिया अलगाव",
          f4Desc: "C++ इंजन को सबप्रोसेस में अलग रखा गया है।",
          f5Title: "मोबाइल सुरक्षा",
          f5Desc: "WakeLock और Doze मोड सुरक्षा अंतर्निहित।",
          f6Title: "दोहरा पारिस्थितिकी तंत्र",
          f6Desc: "पायथन और Node.js दोनों में समान API उपलब्ध।"
        }
      },
      installation: {
        title: "स्थापना निर्देशिका",
        subtitle: "बिना किसी संकलन समस्या के एंड्रॉइड Termux में termux-stt सेट करें।",
        prereqTitle: "Termux पूर्व-आवश्यकताएं",
        pkgTitle: "पैकेज स्थापना",
        androidTweaksTitle: "एंड्रॉइड वातावरण अनुकूलन (अनुशंसित)",
        verifyTitle: "सत्यापन"
      },
      quickstart: {
        title: "त्वरित शुरुआत और व्यंजन विधि",
        subtitle: "ऑडियो ट्रांसक्रिप्शन वर्कफ़्लो के लिए उत्पादन-तैयार कोड स्निपेट।",
        r1Title: "विधि 1: सरल फ़ाइल ट्रांसक्रिप्शन",
        r2Title: "विधि 2: रीयलटाइम माइक्रोफ़ोन स्ट्रीमिंग",
        r3Title: "विधि 3: स्पीकर डायराइजेशन (मीटिंग मिनट्स)",
        r4Title: "विधि 4: बैच प्रोसेसिंग निर्देशिका"
      },
      models: {
        title: "मॉडल हब और रजिस्ट्री",
        subtitle: "SHA-256 अखंडता जांच और स्वचालित डाउनलोडिंग वाले हल्के ऑन-डिवाइस मॉडल।",
        whisperTitle: "Whisper मॉडल (GGML क्वांटाइज्ड)",
        voskTitle: "Vosk मॉडल (X-Vector & STT)",
        sherpaTitle: "Sherpa-ONNX मॉडल",
        cliTitle: "CLI मॉडल प्रबंधन कमांड"
      },
      advancedParams: {
        title: "उन्नत पैरामीटर हैंडबुक",
        subtitle: "अनुमान गति, मेमोरी फ़ुटप्रिंट, VAD संवेदनशीलता और क्लस्टरिंग सटीकता को फाइन-ट्यून करें।",
        vadTitle: "1. VAD और मौन थ्रेसहोल्ड",
        threadTitle: "2. CPU थ्रेड अनुकूलन",
        quantTitle: "3. क्वांटाइजेशन स्तर",
        clusterTitle: "4. डायराइजेशन क्लस्टरिंग पैरामीटर"
      },
      apiReference: {
        title: "100% पूर्ण API संदर्भ",
        subtitle: "पायथन SDK, Node.js SDK और CLI कमांड के लिए पूर्ण विनिर्देश।",
        pythonTitle: "Python SDK (termux_stt)",
        nodeTitle: "Node.js SDK (termux-stt)",
        cliTitle: "CLI कमांड"
      },
      benchmarks: {
        title: "अनुभवजन्य बेंचमार्क और हार्डवेयर",
        subtitle: "सैमसंग गैलेक्सी A35 5G (Exynos 1380, 6GB RAM, Android 14) पर मापा गया।",
        specTitle: "परीक्षण हार्डवेयर वातावरण",
        matrixTitle: "अनुभवजन्य बेंचमार्क मैट्रिक्स",
        findingsTitle: "प्रमुख अनुभवजन्य निष्कर्ष"
      },
      versions: {
        title: "संस्करण पुरालेख और रिलीज नोट्स",
        subtitle: "termux-stt के लिए रिलीज इतिहास और अपग्रेड गाइड।",
        v100Title: "v1.0.0 (प्रारंभिक सार्वजनिक रिलीज) - 2026-08-20"
      }
    }
  };

  if (global.I18n) {
    global.I18n.registerTranslations(translations);
  } else {
    document.addEventListener('DOMContentLoaded', () => {
      if (global.I18n) global.I18n.registerTranslations(translations);
    });
  }
})(window);

