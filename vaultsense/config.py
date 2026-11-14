from dataclasses import dataclass
import os

@dataclass
class VaultSenseConfig:
    volume_mount: str = os.getenv("UGOS_VOLUME_MOUNT", "./data")
    canary_dir: str = os.getenv("UGOS_CANARY_DIR", "./data/.canary_traps")
    entropy_threshold: float = float(os.getenv("ENTROPY_THRESHOLD", "7.85"))
    chunk_size_kb: int = int(os.getenv("DEDUP_CHUNK_SIZE_KB", "64"))
    similarity_threshold: float = 0.85
    min_canary_files: int = 5
    max_scan_workers: int = 4

config = VaultSenseConfig()
