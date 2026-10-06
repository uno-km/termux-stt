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
        shared_dir = os.path.expanduser("~/.cache/termux-ai/models/")
        engine_dir = os.path.join(cls.CACHE_DIR, engine)
        os.makedirs(engine_dir, exist_ok=True)
        # 1. Handle aliases from registry (e.g. turbo -> ggml-large-v3-turbo-q5_0.bin)
        from .registry import MODEL_REGISTRY
        reg = MODEL_REGISTRY.get(engine, {})
        if model_name in reg and "url" in reg[model_name]:
            canon_name = reg[model_name]["url"].split("/")[-1]
            if os.path.exists(os.path.join(shared_dir, canon_name)):
                return os.path.join(shared_dir, canon_name)
            canon_path = os.path.join(engine_dir, canon_name)
            if os.path.exists(canon_path):
                return canon_path
            # Check if already extracted
            for ext in (".tar.bz2", ".tar.gz", ".zip", ".tar"):
                if canon_name.endswith(ext):
                    extracted_path = os.path.join(engine_dir, canon_name[:-len(ext)])
                    if os.path.exists(extracted_path):
                        return extracted_path
            # Check if direct model_name exists in engine_dir
            model_name_path = os.path.join(engine_dir, model_name)
            if os.path.exists(model_name_path):
                return model_name_path
            return canon_path

        # If "small" requested and only small-q5_1 exists
        if model_name == "small":
            if os.path.exists(os.path.join(shared_dir, "ggml-small-q5_1.bin")):
                return os.path.join(shared_dir, "ggml-small-q5_1.bin")
            q5_path = os.path.join(engine_dir, "ggml-small-q5_1.bin")
            if os.path.exists(q5_path):
                return q5_path
        # Handle filenames like ggml-base.bin or just "base"
        filename = model_name
        if engine == "whisper" and not filename.endswith(".bin"):
            filename = f"ggml-{model_name}.bin"
        if os.path.exists(os.path.join(shared_dir, filename)):
            return os.path.join(shared_dir, filename)
        return os.path.join(engine_dir, filename)

    @classmethod
    def check_model_installed(cls, engine: str, model_name: str) -> bool:
        """Check whether a model is already downloaded locally."""
        if not model_name:
            return False
        if os.path.exists(model_name):
            return True
        path = cls._get_model_path(engine, model_name)
        return os.path.exists(path) and (os.path.isdir(path) or os.path.getsize(path) > 0)

    @classmethod
    def ensure_model_interactive(cls, engine: str, model_name: str) -> bool:
        """Prompt user interactively to download model if missing, or auto-download."""
        if cls.check_model_installed(engine, model_name):
            return True

        from .registry import get_model_info
        info = {}
        try:
            reg_key = model_name.replace("ggml-", "").replace(".bin", "").strip()
            info = get_model_info(engine, reg_key)
        except Exception:
            pass

        size_str = info.get("size", "Unknown size")
        desc_str = info.get("description", model_name)

        print("\n" + "=" * 65)
        print(f"[!] Target model '{model_name}' for engine '{engine}' is not downloaded yet.")
        print(f"    - Approximate Size: ~{size_str}")
        print(f"    - Description: {desc_str}")
        print("=" * 65)

        import sys
        if sys.stdin.isatty():
            try:
                choice = input(f"Would you like to download '{model_name}' now? [Y/n]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled.")
                sys.exit(1)

            if choice in ("", "y", "yes"):
                print(f"\n[*] Starting download for '{model_name}'...")
                cls.ensure_model(engine, model_name)
                print(f"[+] Model '{model_name}' successfully provisioned!\n")
                return True
            else:
                print(f"\n[-] Model download skipped. To download manually, run:")
                print(f"    termux-stt models download {engine} --model {model_name}\n")
                sys.exit(1)
        else:
            print(f"[*] Non-interactive environment detected. Auto-provisioning model '{model_name}'...")
            cls.ensure_model(engine, model_name)
            return True

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
        """Download model via HTTP with urllib and atomic .part isolation."""
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        part_dest = dest + ".part"
        if os.path.exists(part_dest):
            try:
                os.remove(part_dest)
            except OSError:
                pass

        print(f"Downloading model from {url} to {dest}...")

        import ssl
        ctx = ssl.create_default_context()
        headers = {"User-Agent": "termux-stt/1.1.3"}
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as response, open(part_dest, 'wb') as out_file:
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

            if sha256 and not cls.verify_integrity(part_dest, sha256):
                if os.path.exists(part_dest):
                    os.remove(part_dest)
                raise ValueError(f"Checksum verification failed for {dest}")

            if os.path.exists(dest):
                os.remove(dest)
            os.replace(part_dest, dest)
            return dest
        except Exception:
            if os.path.exists(part_dest):
                try:
                    os.remove(part_dest)
                except OSError:
                    pass
            raise

    @classmethod
    def ensure_model(cls, engine: str, model_name: str, url: str = "", sha256: str = "") -> str:
        """Get model path, downloading it if necessary."""
        # 1. Direct local file or directory path support (Custom fine-tuned / ONNX model folders / GGML models)
        if os.path.exists(model_name):
            return os.path.abspath(model_name)

        dest = cls._get_model_path(engine, model_name)
        if os.path.exists(dest) and (os.path.isdir(dest) or os.path.getsize(dest) > 0):
            if os.path.isfile(dest):
                extracted = cls._maybe_extract_archive(dest)
                if extracted:
                    return extracted
            if sha256 and not cls.verify_integrity(dest, sha256):
                print("Model corrupted, redownloading...")
                return cls.download_model(url, dest, sha256)
            return dest

        # If URL not provided, look up from registry
        candidate_urls = []
        if url:
            candidate_urls.append(url)
        else:
            reg_name = model_name.replace("ggml-", "").replace(".bin", "").strip()
            try:
                info = get_model_info(engine, reg_name)
                primary_url = info.get("url", "")
                fallback_url = info.get("fallback_url", "")
                if primary_url:
                    candidate_urls.append(primary_url)
                if fallback_url:
                    candidate_urls.append(fallback_url)
                sha256 = sha256 or info.get("sha256", "")
            except ValueError:
                import difflib

                from .registry import MODEL_REGISTRY
                known_models = list(MODEL_REGISTRY.get(engine, {}).keys())
                matches = difflib.get_close_matches(reg_name, known_models, n=3, cutoff=0.4)

                msg_lines = [f"[ERROR] Model '{model_name}' is not recognized for engine '{engine}'."]
                if matches:
                    msg_lines.append("\nDid you mean:\n  - " + "\n  - ".join(matches))

                if known_models:
                    msg_lines.append(f"\nAvailable models for '{engine}':")
                    for km in known_models:
                        km_info = MODEL_REGISTRY[engine][km]
                        size_str = f" ({km_info.get('size', '')})" if km_info.get('size') else ""
                        desc_str = f" - {km_info.get('description', '')}" if km_info.get('description') else ""
                        msg_lines.append(f"  - {km}{size_str}{desc_str}")

                raise ValueError("\n".join(msg_lines))

        if not candidate_urls:
            raise ValueError(f"Model '{model_name}' for engine '{engine}' not found and no URL provided.")

        last_err = None
        for cand_url in candidate_urls:
            try:
                downloaded_file = cls.download_model(cand_url, dest, sha256)
                # Unpack archives if tar.bz2 / tar.gz / zip
                extracted_dir = cls._maybe_extract_archive(downloaded_file)
                return extracted_dir or downloaded_file
            except Exception as exc:
                last_err = exc
                print(f"[-] Mirror download failed for {cand_url}: {exc}")
                continue

        raise ValueError(f"Failed to download model '{model_name}' from any candidate URL: {last_err}")

    @classmethod
    def _maybe_extract_archive(cls, archive_path: str) -> Optional[str]:
        """Extract tar.bz2, tar.gz, or zip archive if not already extracted."""
        if not archive_path or not os.path.exists(archive_path):
            return None
        if os.path.isdir(archive_path):
            return archive_path

        import tarfile
        import zipfile
        base_dir = os.path.dirname(archive_path)
        archive_name = os.path.basename(archive_path)

        target_folder = None
        for ext in (".tar.bz2", ".tar.gz", ".zip", ".tar"):
            if archive_name.endswith(ext):
                target_folder = archive_name[:-len(ext)]
                break

        is_tar = tarfile.is_tarfile(archive_path) if os.path.isfile(archive_path) else False
        is_zip = zipfile.is_zipfile(archive_path) if os.path.isfile(archive_path) else False

        if not target_folder:
            if is_tar or is_zip:
                target_folder = archive_name + "-extracted"
            else:
                return None

        extract_dest = os.path.join(base_dir, target_folder)
        if os.path.exists(extract_dest) and os.path.isdir(extract_dest) and os.listdir(extract_dest):
            return extract_dest

        print(f"Extracting archive {archive_path} to {extract_dest}...")
        os.makedirs(extract_dest, exist_ok=True)
        if is_tar or archive_name.endswith((".tar.bz2", ".tar.gz", ".tar")):
            mode = "r:bz2" if archive_name.endswith(".tar.bz2") else ("r:gz" if archive_name.endswith(".tar.gz") else "r:*")
            with tarfile.open(archive_path, mode) as tar:
                tar.extractall(path=extract_dest)
        elif is_zip or archive_name.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zf:
                zf.extractall(path=extract_dest)

        # If archive had a single top-level folder, point to it
        entries = os.listdir(extract_dest)
        if len(entries) == 1 and os.path.isdir(os.path.join(extract_dest, entries[0])):
            return os.path.join(extract_dest, entries[0])

        return extract_dest

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
