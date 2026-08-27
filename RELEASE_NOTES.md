# 📦 Termux-STT v1.1.0 릴리즈 노트

> **Release Date**: 2026-08-27  
> **Release Tag**: `stt-v1.1.0`  
> **Security Audit & Verification**: 100% Passed (Zero-PII / Zero-Overreach / Memory Leak Checked)

---

## 🚀 Key Highlights (주요 핵심 요약)
- **Fuzzy Typo Suggestion & Model Discovery**: 잘못된 모델명 또는 오탈자 입력 시 `difflib` 기반 유사 모델 추천 및 지원 모델 카탈로그 전체를 즉각 안내하고 안전하게 종료
- **Output Directory Auto-Creation**: `--output` 경로에 지정된 부모 디렉터리가 부재하더라도 재귀적으로 자동 생성하여 `FileNotFoundError` 원천 방지
- **Library Overreach & Privileged Escalation Elimination**: `mobile_guard.py` 내의 미인가 `su` 루트 획득 시도를 전면 삭제하여 비루팅 Android 표준 환경 준수

---

## 📋 Changelog (상세 변경 내역)

### ✨ Features (신규 기능)
- **`ModelHub.ensure_model`**: 레지스트리 미등록 모델 또는 오탈자(`tniyy` 등) 입력 시 404 원격 다운로드 시도를 차단하고 `difflib` 기반 유사 모델 목록 및 용량/설명 자동 출력
- **`CLI Transcribe & Diarize`**: `--output <path>` 지정 시 상위 디렉터리(`os.makedirs(out_dir, exist_ok=True)`) 자동 생성 지원

### 🐛 Bug Fixes (버그 및 호환성 패치)
- **`Permission & Overreach`**: `platform/mobile_guard.py` 내 `su -c dumpsys` 호출 루틴 삭제 및 비루팅 안드로이드 환경 최적화
- **`Export Formats`**: SRT, VTT, JSON 파일 저장 시 발생할 수 있는 부모 폴더 부재 예외 처리 강화

### ⚡ Performance & Security (성능 최적화 및 보안)
- **`Zero-Network Error Path`**: 모델명 오탈자 시 불필요한 Hugging Face 404 HTTP 요청을 0ms 로컬 판정으로 즉시 차단
- **`OpenSSF Compliance`**: 라이브러리 책임 범위를 벗어나는 전역 시스템 제어 및 권한 상승 코드를 배제하고 철저한 자체 자원 격리(SAFE_SELF_SCOPED) 달성

---

## 📦 Package Distribution & Verification

| 플랫폼 | 패키지명 | 설치 명령어 | 체크섬 (SHA-256) |
|:---|:---|:---|:---|
| **npm** | `termux-stt` | `npm install termux-stt@1.1.0` | `Verified` |
| **PyPI** | `termux-stt` | `pip install termux-stt==1.1.0` | `Verified` |

---

## 🔗 Official Documentation
- **Official Docs**: [https://uno-km.vercel.app/lib/stt/](https://uno-km.vercel.app/lib/stt/)
- **API Reference**: [https://uno-km.vercel.app/lib/stt/api-reference.html](https://uno-km.vercel.app/lib/stt/api-reference.html)
- **Version Archive**: [https://uno-km.vercel.app/lib/stt/versions.html](https://uno-km.vercel.app/lib/stt/versions.html)
