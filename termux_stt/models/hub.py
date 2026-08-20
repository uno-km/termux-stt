"""
Model download and caching hub.
"""

import os
import urllib.request
import hashlib
from typing import List, Dict, Optional
from pathlib import Path

from .registry import get_model_info

__all__ = ["ModelHub"]


class ModelHub:
    """Manages model downloading and caching."""

    CACHE_DIR = os.path.expanduser("~/.cache/termux-stt/models/")

    @classmethod
    def _get_model_path(cls, engine: str, model_name: str) -> str:
        engine_dir = os.path.join(cls.CACHE_DIR, engine)
        os.makedirs(engine_dir, exist_ok=True)
        # Handle filenames like ggml-base.bin or just "base"
        filename = model_name
        if engine == "whisper" and not filename.endswith(".bin"):
            filename = f"ggml-{model_name}.bin"
        return os.path.join(engine_dir, filename)

    @classmethod
    def verify_integrity(cls, path: str, expected_sha256: str) -> bool:
        """Verify SHA256 checksum of a file."""
        if not os.path.exists(path) or not expected_sha256:
            return True
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() == expected_sha256

    @classmethod
    def download_model(cls, url: str, dest: str, sha256: Optional[str] = None) -> str:
        """Download model via HTTP with urllib."""
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        print(f"Downloading model from {url} to {dest}...")

        headers = {"User-Agent": "termux-stt/1.0.0"}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 65536
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                if total_size > 0:
                    percent = int(downloaded * 100 / total_size)
                    if percent % 20 == 0:
                        print(f"\rDownloading: {percent}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)", end="", flush=True)

        print("\nDownload complete.")

        if sha256 and not cls.verify_integrity(dest, sha256):
            if os.path.exists(dest):
                os.remove(dest)
            raise ValueError(f"Checksum verification failed for {dest}")

        return dest

    @classmethod
    def ensure_model(cls, engine: str, model_name: str, url: str = "", sha256: str = "") -> str:
        """Get model path, downloading it if necessary."""
        dest = cls._get_model_path(engine, model_name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            if sha256 and not cls.verify_integrity(dest, sha256):
                print("Model corrupted, redownloading...")
                return cls.download_model(url, dest, sha256)
            return dest

        # If URL not provided, look up from registry
        if not url:
            try:
                # Strip ggml- prefix or .bin suffix if present for registry lookup
                reg_name = model_name.replace("ggml-", "").replace(".bin", "")
                info = get_model_info(engine, reg_name)
                url = info.get("url", "")
                sha256 = sha256 or info.get("sha256", "")
            except Exception:
                pass

        if not url:
            # Fallback for whisper standard models
            if engine == "whisper":
                base_name = model_name.replace("ggml-", "").replace(".bin", "")
                url = f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{base_name}.bin"

        if not url:
            raise ValueError(f"Model '{model_name}' for engine '{engine}' not found and no URL provided.")

        return cls.download_model(url, dest, sha256)

    @classmethod
    def list_cached_models(cls) -> List[Dict[str, str]]:
        """List all models currently in cache."""
        models = []
        if not os.path.exists(cls.CACHE_DIR):
            return models
        for engine in os.listdir(cls.CACHE_DIR):
            engine_path = os.path.join(cls.CACHE_DIR, engine)
            if os.path.isdir(engine_path):
                for model in os.listdir(engine_path):
                    models.append({"engine": engine, "model_name": model})
        return models

    @classmethod
    def remove_model(cls, engine: str, model_name: str) -> bool:
        """Remove a cached model."""
        path = cls._get_model_path(engine, model_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
