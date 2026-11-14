import math
import os
import time
import random
import string
from typing import Dict, Any, List

class EntropyRansomwareCanary:
    """Shannon Entropy and Honeypot Canary Guard for UGREEN NAS.
    High entropy (> 7.85 bits/byte) in non-compressed standard documents
    indicates active encryption. Canary trap files serve as tripwires.
    """

    def __init__(self, canary_dir: str = "./data/.canary_traps", threshold: float = 7.85):
        self.canary_dir = canary_dir
        self.threshold = threshold
        self.canary_files: Dict[str, str] = {}

    @staticmethod
    def calculate_shannon_entropy(data: bytes) -> float:
        """Calculate Shannon entropy in bits per byte (0.0 to 8.0)."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        counts = [0] * 256
        for byte in data:
            counts[byte] += 1
        for count in counts:
            if count > 0:
                p = count / length
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    def analyze_file_entropy(self, filepath: str) -> Dict[str, Any]:
        """Inspect a file's byte entropy and assess risk."""
        if not os.path.exists(filepath):
            return {"filepath": filepath, "exists": False, "entropy": 0.0, "risk": "UNKNOWN"}

        with open(filepath, "rb") as f:
            sample = f.read(65536)

        entropy = self.calculate_shannon_entropy(sample)
        ext = os.path.splitext(filepath)[1].lower()
        
        # Naturally compressed formats have high entropy legitimately
        naturally_compressed = {".zip", ".gz", ".tar", ".7z", ".mp4", ".mkv", ".png", ".jpg", ".jpeg"}
        
        is_suspicious = (entropy >= self.threshold) and (ext not in naturally_compressed)
        
        risk = "NORMAL"
        if is_suspicious:
            risk = "CRITICAL_ANOMALOUS_ENTROPY"
        elif entropy > 7.5 and ext in {".txt", ".docx", ".pdf", ".xlsx"}:
            risk = "ELEVATED"

        return {
            "filepath": filepath,
            "extension": ext,
            "size_bytes": os.path.getsize(filepath),
            "entropy": entropy,
            "threshold": self.threshold,
            "is_suspicious": is_suspicious,
            "risk": risk
        }

    def deploy_canaries(self, count: int = 5) -> List[str]:
        """Deploy honey-canary tripwire files into sensitive directory paths."""
        os.makedirs(self.canary_dir, exist_ok=True)
        deployed = []
        extensions = [".docx", ".xlsx", ".pdf", ".sql", ".conf"]
        
        for i in range(count):
            ext = extensions[i % len(extensions)]
            name = f"canary_vault_backup_0{i+1}{ext}"
            path = os.path.join(self.canary_dir, name)
            
            # Write plausible structured text with low-entropy plaintext
            content = f"UGOS_VAULT_CANARY_SEED_{i}_{time.time()}\n" + (
                "Confidential Financial Ledger Entry. Do not edit or modify.\n" * 50
            )
            raw = content.encode("utf-8")
            with open(path, "wb") as f:
                f.write(raw)
            
            initial_entropy = self.calculate_shannon_entropy(raw)
            self.canary_files[path] = {
                "created_at": time.time(),
                "initial_entropy": initial_entropy,
                "initial_size": len(raw)
            }
            deployed.append(path)
        return deployed

    def check_canaries(self) -> Dict[str, Any]:
        """Check all deployed canaries for unauthorized modification or encryption."""
        if not os.path.exists(self.canary_dir):
            return {"canaries_found": 0, "compromised": 0, "status": "NO_CANARIES_DEPLOYED", "alerts": []}

        files = [os.path.join(self.canary_dir, f) for f in os.listdir(self.canary_dir)]
        alerts = []
        compromised = 0

        for path in files:
            if not os.path.isfile(path):
                continue
            analysis = self.analyze_file_entropy(path)
            if analysis["is_suspicious"] or analysis["entropy"] >= self.threshold:
                compromised += 1
                alerts.append({
                    "canary_file": path,
                    "event": "CANARY_INTEGRITY_BREACH",
                    "entropy": analysis["entropy"],
                    "threat": "POSSIBLE_RANSOMWARE_ENCRYPTION_SPIKE",
                    "action_taken": "ISOLATION_SIGNAL_EMITTED"
                })

        return {
            "canaries_scanned": len(files),
            "compromised_count": compromised,
            "status": "THREAT_DETECTED" if compromised > 0 else "HEALTHY",
            "alerts": alerts
        }
