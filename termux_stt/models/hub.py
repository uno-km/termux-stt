"""
Model download and caching hub.
"""

import os
import urllib.request
import hashlib
from typing import List, Dict, Optional

__all__ = ["ModelHub"]

class ModelHub:
    """Manages model downloading and caching."""
    
    CACHE_DIR = os.path.expanduser("~/.cache/termux-stt/models/")
    
    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        
    def _get_model_path(self, engine: str, model_name: str) -> str:
        engine_dir = os.path.join(self.CACHE_DIR, engine)
        os.makedirs(engine_dir, exist_ok=True)
        return os.path.join(engine_dir, model_name)

    def verify_integrity(self, path: str, expected_sha256: str) -> bool:
        """Verify SHA256 checksum of a file."""
        if not os.path.exists(path):
            return False
            
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() == expected_sha256

    def download_model(self, url: str, dest: str, sha256: Optional[str] = None) -> str:
        """Download model via HTTP with urllib."""
        print(f"Downloading {url} to {dest}...")
        
        # Simple reporter
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                if percent % 10 == 0:
                    print(f"\rProgress: {percent}%", end="")
                    
        urllib.request.urlretrieve(url, dest, reporthook=reporthook)
        print("\nDownload complete.")
        
        if sha256 and not self.verify_integrity(dest, sha256):
            os.remove(dest)
            raise ValueError("Checksum verification failed after download.")
            
        return dest

    def ensure_model(self, engine: str, model_name: str, url: str = "", sha256: str = "") -> str:
        """Get model path, downloading it if necessary."""
        dest = self._get_model_path(engine, model_name)
        if os.path.exists(dest):
            if sha256 and not self.verify_integrity(dest, sha256):
                print("Model corrupted, redownloading...")
                return self.download_model(url, dest, sha256)
            return dest
            
        if not url:
            raise ValueError(f"Model {model_name} not found and no URL provided.")
            
        return self.download_model(url, dest, sha256)

    def list_cached_models(self) -> List[Dict[str, str]]:
        """List all models currently in cache."""
        models = []
        if not os.path.exists(self.CACHE_DIR):
            return models
        for engine in os.listdir(self.CACHE_DIR):
            engine_path = os.path.join(self.CACHE_DIR, engine)
            if os.path.isdir(engine_path):
                for model in os.listdir(engine_path):
                    models.append({"engine": engine, "model_name": model})
        return models

    def remove_model(self, engine: str, model_name: str) -> bool:
        """Remove a cached model."""
        path = self._get_model_path(engine, model_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
