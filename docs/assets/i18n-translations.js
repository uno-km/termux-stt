/**
 * AMEVA Ecosystem - Multilingual Translation Dictionary (6 Languages)
 * English (en), Korean (ko), Japanese (ja), Chinese (zh), Spanish (es), Hindi (hi)
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
