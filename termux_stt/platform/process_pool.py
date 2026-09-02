import logging
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

@dataclass
class SubprocessResult:
    returncode: int
    stdout: str
    stderr: str
    duration_sec: float

def run_isolated(cmd: List[str], timeout: Optional[float] = None, env: Optional[Dict[str, str]] = None, max_retries: int = 2) -> SubprocessResult:
    """Run a subprocess in isolation, handling crashes and retries."""
    for attempt in range(max_retries):
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                check=False
            )
            duration = time.time() - start_time
            if result.returncode < 0:
                # E.g., -11 for SIGSEGV
                logger.error(f"Process crashed with signal {-result.returncode}. Attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    continue

            return SubprocessResult(
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration_sec=duration
            )
        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            logger.error(f"Process timed out after {duration:.2f}s")
            if attempt < max_retries - 1:
                continue
            return SubprocessResult(
                returncode=-1,
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or ""),
                duration_sec=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            logger.exception("Unexpected error running subprocess")
            if attempt < max_retries - 1:
                continue
            return SubprocessResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
                duration_sec=duration
            )

    return SubprocessResult(-1, "", "Failed after retries", 0.0)
