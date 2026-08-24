// AMEVA Auto-Generated i18n Dictionary
if (window.i18nManager) {
  window.i18nManager.registerTranslations({
  "en": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPI (pip)",
      "npmBtn": "npm (Node.js)",
      "githubBtn": "GitHub",
      "footerText": "© 2026 AMEVA Open-Source Foundation. Released under the Apache-2.0 License.",
      "nav": {
        "overview": "Overview",
        "reference": "Official Reference",
        "ecosystem": "AMEVA Ecosystem",
        "aiSpecs": "AI Agent Protocols",
        "home": "Home / Architecture",
        "installation": "Installation Guide",
        "quickstart": "Quickstart & Recipes",
        "apiReference": "API Reference",
        "benchmarks": "Benchmarks & Profiling",
        "advancedParams": "Advanced Parameters",
        "versions": "Version Archive"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "Unified On-Device Speech-to-Text & Pure Python 128d X-Vector Speaker Diarization",
      "quickInstallTitle": "1-Line Quick Installation",
      "quickInstallDesc": "Install the official package directly into your runtime:",
      "challengeTitle": "The Engineering Challenge",
      "challengeText": "Transcribing and diarizing multi-speaker conversations on edge devices typically demands heavy PyTorch runtimes (>2GB) and severe GPU memory consumption.",
      "breakthroughTitle": "The Architectural Breakthrough",
      "breakthroughText": "Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM.",
      "featuresTitle": "Key Capabilities & Built-in Hardening",
      "matrixTitle": "Supported Compute Kernels & Operations",
      "matrixCol1": "Subsystem Category",
      "matrixCol2": "Operations & Kernels",
      "matrixCol3": "Status",
      "codeExampleTitle": "Canonical Usage Example",
      "nextStepsTitle": "Getting Started & Deep Guides",
      "linkInstall": "Detailed Installation Guide (Hardware dependencies, Termux setup, WebGPU flags)",
      "linkQuickstart": "Quickstart Recipes & Common Execution Patterns",
      "linkApi": "100% Full API Reference & Struct Definitions",
      "features": {
        "0": {
          "title": "Triple STT Engine Integration",
          "desc": "Seamlessly switches between Whisper.cpp (accuracy), Vosk (latency), and Sherpa-ONNX."
        },
        "1": {
          "title": "Pure Python Speaker Diarization",
          "desc": "Lightweight cosine spectral clustering without external ML frameworks."
        },
        "2": {
          "title": "Zero Cloud Egress Audio Privacy",
          "desc": "Audio processing and transcription execute strictly on-device without cloud network calls."
        }
      }
    }
  },
  "ko": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPI 패키지",
      "npmBtn": "npm 패키지",
      "githubBtn": "GitHub 저장소",
      "footerText": "© 2026 AMEVA 오픈소스 재단. Apache-2.0 라이선스로 배포됨.",
      "nav": {
        "overview": "개요",
        "reference": "공식 레퍼런스",
        "ecosystem": "AMEVA 생태계",
        "aiSpecs": "AI 에이전트 프로토콜",
        "home": "홈 / 아키텍처",
        "installation": "설치 가이드",
        "quickstart": "퀵스타트 & 레시피",
        "apiReference": "전체 API 명세",
        "benchmarks": "벤치마크 & 하드웨어",
        "advancedParams": "고급 파라미터",
        "versions": "버전 아카이브"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "통합 온디바이스 음성인식(STT) 및 순수 Python 128d X-Vector 화자 분리 프레임워크",
      "quickInstallTitle": "1줄 빠른 설치",
      "quickInstallDesc": "환경에 맞는 공식 패키지를 즉시 설치하세요:",
      "challengeTitle": "엔지니어링 도전 과제",
      "challengeText": "모바일 단말기에서 다중 화자 음성 인식 및 화자 분리를 수행하려면 2GB 이상의 무거운 PyTorch와 대용량 GPU 메모리를 요구합니다.",
      "breakthroughTitle": "아키텍처 혁신 및 해결책",
      "breakthroughText": "Whisper.cpp, Vosk, Sherpa-ONNX 3대 엔진을 통합하고, 닫힌 형태 순수 Python 128차원 X-Vector 클러스터링을 결합하여 80MB 미만의 메모리로 실시간 화자 분리를 구현합니다.",
      "featuresTitle": "핵심 역량 및 빌트인 보안/안정성",
      "matrixTitle": "지원 연산 커널 및 모듈 매트릭스",
      "matrixCol1": "서브시스템 분류",
      "matrixCol2": "지원 연산 및 커널",
      "matrixCol3": "상태",
      "codeExampleTitle": "정석 사용법 코드 예제",
      "nextStepsTitle": "시작하기 & 심층 가이드",
      "linkInstall": "상세 설치 가이드 (하드웨어 의존성, Termux 설정, WebGPU 플래그)",
      "linkQuickstart": "퀵스타트 레시피 및 주요 실행 패턴",
      "linkApi": "100% 전체 API 명세 및 구조체 정의",
      "features": {
        "0": {
          "title": "3대 STT 엔진 통합 지원",
          "desc": "Whisper.cpp(정밀도), Vosk(초저지연), Sherpa-ONNX 엔진을 상황에 맞게 유연하게 전환합니다."
        },
        "1": {
          "title": "순수 Python 128d 화자 분리 알고리즘",
          "desc": "PyTorch 없이 순수 대수 코사인 스펙트럼 클러스터링으로 화자를 정밀하게 분리합니다."
        },
        "2": {
          "title": "100% 온디바이스 오디오 프라이버시",
          "desc": "모든 음성 스트림과 텍스트 변환이 단말기 로컬 하드웨어에서만 구동되어 데이터 유출을 차단합니다."
        }
      }
    }
  },
  "ja": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPIパッケージ",
      "npmBtn": "npmパッケージ",
      "githubBtn": "GitHub",
      "footerText": "© 2026 AMEVA Open-Source Foundation. Apache-2.0 ライセンスの下で公開。",
      "nav": {
        "overview": "概要",
        "reference": "公式リファレンス",
        "ecosystem": "AMEVA エコシステム",
        "aiSpecs": "AIエージェント仕様",
        "home": "ホーム / アーキテクチャ",
        "installation": "インストールガイド",
        "quickstart": "クイックスタート",
        "apiReference": "APIリファレンス",
        "benchmarks": "ベンチマーク",
        "advancedParams": "詳細パラメータ",
        "versions": "バージョン履歴"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "Unified On-Device Speech-to-Text & Pure Python 128d X-Vector Speaker Diarization",
      "quickInstallTitle": "1行クイックインストール",
      "quickInstallDesc": "ランタイムに公式パッケージを直接インストールします:",
      "challengeTitle": "技術的課題",
      "challengeText": "Transcribing and diarizing multi-speaker conversations on edge devices typically demands heavy PyTorch runtimes (>2GB) and severe GPU memory consumption.",
      "breakthroughTitle": "アーキテクチャのブレークスルー",
      "breakthroughText": "Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM.",
      "featuresTitle": "コア機能と安定性",
      "matrixTitle": "サポートされている演算とカーネル",
      "matrixCol1": "サブシステム区分",
      "matrixCol2": "サポート演算",
      "matrixCol3": "状態",
      "codeExampleTitle": "標準的なコード例",
      "nextStepsTitle": "はじめに",
      "linkInstall": "詳細インストールガイド",
      "linkQuickstart": "クイックスタートレシピ",
      "linkApi": "API仕様書"
    }
  },
  "zh": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPI (pip)",
      "npmBtn": "npm (Node.js)",
      "githubBtn": "GitHub",
      "footerText": "© 2026 AMEVA 开源基金会。在 Apache-2.0 许可下发布。",
      "nav": {
        "overview": "概述",
        "reference": "官方参考",
        "ecosystem": "AMEVA 生态系统",
        "aiSpecs": "AI 协议",
        "home": "主页 / 架构",
        "installation": "安装指南",
        "quickstart": "快速入门",
        "apiReference": "API 参考",
        "benchmarks": "基准测试",
        "advancedParams": "高级参数",
        "versions": "版本归档"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "Unified On-Device Speech-to-Text & Pure Python 128d X-Vector Speaker Diarization",
      "quickInstallTitle": "一键快速安装",
      "quickInstallDesc": "直接将官方包安装到您的环境中:",
      "challengeTitle": "工程挑战",
      "challengeText": "Transcribing and diarizing multi-speaker conversations on edge devices typically demands heavy PyTorch runtimes (>2GB) and severe GPU memory consumption.",
      "breakthroughTitle": "架构突破",
      "breakthroughText": "Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM.",
      "featuresTitle": "核心特性与加固",
      "matrixTitle": "支持的计算内核与操作",
      "matrixCol1": "分类",
      "matrixCol2": "操作与模块",
      "matrixCol3": "状态",
      "codeExampleTitle": "标准代码示例",
      "nextStepsTitle": "开始使用",
      "linkInstall": "详细安装指南",
      "linkQuickstart": "快速入门方案",
      "linkApi": "完整 API 规范"
    }
  },
  "es": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPI (pip)",
      "npmBtn": "npm (Node.js)",
      "githubBtn": "GitHub",
      "footerText": "© 2026 Fundación AMEVA. Licencia Apache-2.0.",
      "nav": {
        "overview": "Visión General",
        "reference": "Referencia Oficial",
        "ecosystem": "Ecosistema AMEVA",
        "aiSpecs": "Protocolos de IA",
        "home": "Inicio / Arquitectura",
        "installation": "Guía de Instalación",
        "quickstart": "Inicio Rápido",
        "apiReference": "Referencia de API",
        "benchmarks": "Evaluaciones de Rendimiento",
        "advancedParams": "Parámetros Avanzados",
        "versions": "Archivo de Versiones"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "Unified On-Device Speech-to-Text & Pure Python 128d X-Vector Speaker Diarization",
      "quickInstallTitle": "Instalación Rápida en 1 Línea",
      "quickInstallDesc": "Instale el paquete oficial directamente en su entorno:",
      "challengeTitle": "El Desafío de Ingeniería",
      "challengeText": "Transcribing and diarizing multi-speaker conversations on edge devices typically demands heavy PyTorch runtimes (>2GB) and severe GPU memory consumption.",
      "breakthroughTitle": "El Avance Arquitectónico",
      "breakthroughText": "Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM.",
      "featuresTitle": "Capacidades Clave y Seguridad",
      "matrixTitle": "Operaciones y Núcleos Soportados",
      "matrixCol1": "Categoría",
      "matrixCol2": "Operaciones",
      "matrixCol3": "Estado",
      "codeExampleTitle": "Ejemplo de Uso Estándar",
      "nextStepsTitle": "Primeros Pasos",
      "linkInstall": "Guía Detallada de Instalación",
      "linkQuickstart": "Recetas de Inicio Rápido",
      "linkApi": "Especificación de API"
    }
  },
  "de": {
    "common": {
      "brand": "Termux-STT",
      "releaseTag": "v1.1.0 (Production Release)",
      "pypiBtn": "PyPI (pip)",
      "npmBtn": "npm (Node.js)",
      "githubBtn": "GitHub",
      "footerText": "© 2026 AMEVA Open-Source Foundation. Lizenziert unter Apache-2.0.",
      "nav": {
        "overview": "Überblick",
        "reference": "Offizielle Referenz",
        "ecosystem": "AMEVA Ökosystem",
        "aiSpecs": "KI-Agenten-Protokolle",
        "home": "Startseite / Architektur",
        "installation": "Installationsanleitung",
        "quickstart": "Schnellstart & Rezepte",
        "apiReference": "API-Referenz",
        "benchmarks": "Benchmarks & Profiling",
        "advancedParams": "Erweiterte Parameter",
        "versions": "Versionsarchiv"
      }
    },
    "home": {
      "title": "Termux-STT",
      "subtitle": "Unified On-Device Speech-to-Text & Pure Python 128d X-Vector Speaker Diarization",
      "quickInstallTitle": "1-Zeilen-Schnellinstallation",
      "quickInstallDesc": "Installieren Sie das offizielle Paket direkt in Ihre Laufzeitumgebung:",
      "challengeTitle": "Die Technische Herausforderung",
      "challengeText": "Transcribing and diarizing multi-speaker conversations on edge devices typically demands heavy PyTorch runtimes (>2GB) and severe GPU memory consumption.",
      "breakthroughTitle": "Der Architektonische Durchbruch",
      "breakthroughText": "Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM.",
      "featuresTitle": "Kernfunktionen & Stabilität",
      "matrixTitle": "Unterstützte Rechenkerne & Operationen",
      "matrixCol1": "Kategorie",
      "matrixCol2": "Operationen",
      "matrixCol3": "Status",
      "codeExampleTitle": "Standard-Codebeispiel",
      "nextStepsTitle": "Erste Schritte",
      "linkInstall": "Detaillierte Installationsanleitung",
      "linkQuickstart": "Schnellstartanleitung",
      "linkApi": "API-Spezifikation"
    }
  }
});
};
