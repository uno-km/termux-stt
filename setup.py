from setuptools import find_packages, setup

setup(
    name="termux-stt",
    version="1.1.5",
    description="Android on-device STT framework for Termux ??whisper.cpp, vosk, sherpa-onnx unified",
    author="Eunho Kim (@uno-km)",
    packages=find_packages(),
    package_data={
        "termux_stt": ["bin/*"],
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "ameva-runtime>=2.0.0",
    ],
    extras_require={
        "dev": ["pytest", "ruff", "mypy"]
    },
    entry_points={
        "console_scripts": [
            "termux-stt = termux_stt.cli.main:main",
            "termux-stt-install = termux_stt.platform.installer:main",
        ]
    }
)
