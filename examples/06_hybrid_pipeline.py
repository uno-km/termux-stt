# examples/06_hybrid_pipeline.py
# 실행 방법: python 06_hybrid_pipeline.py
# Whisper + Vosk 하이브리드 파이프라인.

import termux_stt

def main():
    engine = termux_stt.create_engine("hybrid")
    print("하이브리드 파이프라인 초기화 완료")

if __name__ == "__main__":
    main()
