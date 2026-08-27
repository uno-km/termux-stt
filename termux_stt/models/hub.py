"""
Model download and caching hub.
"""

import hashlib
import os
import urllib.request
from typing import Dict, List, Optional

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

        import ssl
        try:
            ctx = ssl.create_default_context()
        except Exception:
            ctx = None

        def _open_url(request):
            try:
                return urllib.request.urlopen(request, context=ctx)
            except Exception:
                insecure_ctx = ssl._create_unverified_context()
                return urllib.request.urlopen(request, context=insecure_ctx)

        headers = {"User-Agent": "termux-stt/1.0.0"}
        req = urllib.request.Request(url, headers=headers)

        with _open_url(req) as response, open(dest, 'wb') as out_file:
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
        # 1. Direct local file path support (Custom fine-tuned / BitNet / LLaMA / GGML models)
        if os.path.exists(model_name) and os.path.isfile(model_name):
            return os.path.abspath(model_name)

        dest = cls._get_model_path(engine, model_name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            if sha256 and not cls.verify_integrity(dest, sha256):
                print("Model corrupted, redownloading...")
                return cls.download_model(url, dest, sha256)
            return dest

        # If URL not provided, look up from registry
        if not url:
            reg_name = model_name.replace("ggml-", "").replace(".bin", "").strip()
            try:
                info = get_model_info(engine, reg_name)
                url = info.get("url", "")
                sha256 = sha256 or info.get("sha256", "")
            except ValueError:
                import difflib
                from .registry import MODEL_REGISTRY
                known_models = list(MODEL_REGISTRY.get(engine, {}).keys())
                matches = difflib.get_close_matches(reg_name, known_models, n=3, cutoff=0.4)
                
                msg_lines = [f"[ERROR] Model '{model_name}' is not recognized for engine '{engine}'."]
                if matches:
                    msg_lines.append(f"\nDid you mean:\n  - " + "\n  - ".join(matches))
                
                if known_models:
                    msg_lines.append(f"\nAvailable models for '{engine}':")
                    for km in known_models:
                        km_info = MODEL_REGISTRY[engine][km]
                        size_str = f" ({km_info.get('size', '')})" if km_info.get('size') else ""
                        desc_str = f" - {km_info.get('description', '')}" if km_info.get('description') else ""
                        msg_lines.append(f"  - {km}{size_str}{desc_str}")
                        
                raise ValueError("\n".join(msg_lines))

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
