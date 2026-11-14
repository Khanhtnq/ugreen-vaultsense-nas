import hashlib
import os
import math
from typing import List, Dict, Any, Tuple

class SemanticDeduplicator:
    """Zero-Cloud Deduplicator for UGREEN NAS storage pools.
    Combines SHA-256 exact-match with chunk rolling hashes and MinHash
    for near-duplicate text/document detection without external API calls.
    """

    def __init__(self, chunk_size: int = 65536):
        self.chunk_size = chunk_size

    def compute_file_hash(self, filepath: str) -> str:
        """Compute full SHA-256 checksum of a file."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(self.chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    def chunk_fingerprints(self, filepath: str) -> List[str]:
        """Generate rolling chunk hashes for content-defined block comparison."""
        fps = []
        with open(filepath, "rb") as f:
            while chunk := f.read(self.chunk_size):
                fps.append(hashlib.md5(chunk).hexdigest())
        return fps

    def text_minhash(self, text: str, num_perm: int = 32) -> List[int]:
        """Compute MinHash signature for text documents to detect near-duplicates."""
        tokens = set(text.lower().split())
        if not tokens:
            return [0] * num_perm
        
        sig = []
        for i in range(num_perm):
            min_val = float('inf')
            for token in tokens:
                seed_token = f"{i}_{token}".encode('utf-8')
                val = int(hashlib.sha256(seed_token).hexdigest(), 16)
                if val < min_val:
                    min_val = val
            sig.append(min_val % 1000000)
        return sig

    def estimate_jaccard_similarity(self, sig1: List[int], sig2: List[int]) -> float:
        """Estimate Jaccard similarity between two MinHash signatures."""
        if len(sig1) != len(sig2) or not sig1:
            return 0.0
        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return round(matches / len(sig1), 4)

    def scan_directory_for_duplicates(self, root_dir: str) -> Dict[str, Any]:
        """Scan directory and return exact and near duplicates."""
        if not os.path.exists(root_dir):
            return {"exact_duplicates": [], "near_duplicates": [], "scanned_files": 0, "space_reclaimable_bytes": 0}

        hash_map: Dict[str, List[Tuple[str, int]]] = {}
        text_signatures: Dict[str, Tuple[List[int], int]] = {}
        scanned_count = 0
        total_reclaimable = 0

        for root, _, files in os.walk(root_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    fhash = self.compute_file_hash(filepath)
                    hash_map.setdefault(fhash, []).append((filepath, size))
                    scanned_count += 1

                    # Check text files for near-duplication
                    if filename.lower().endswith((".txt", ".md", ".json", ".csv", ".log")):
                        try:
                            with open(filepath, "r", encoding="utf-8", errors="ignore") as tf:
                                text_signatures[filepath] = (self.text_minhash(tf.read(8192)), size)
                        except Exception:
                            pass
                except (OSError, IOError):
                    continue

        exact_dupes = []
        for fhash, paths in hash_map.items():
            if len(paths) > 1:
                original = paths[0]
                dupes = paths[1:]
                waste = sum(sz for _, sz in dupes)
                total_reclaimable += waste
                exact_dupes.append({
                    "hash": fhash,
                    "original": original[0],
                    "size_bytes": original[1],
                    "duplicates": [p[0] for p in dupes],
                    "waste_bytes": waste
                })

        near_dupes = []
        file_list = list(text_signatures.items())
        for i in range(len(file_list)):
            for j in range(i + 1, len(file_list)):
                path1, (sig1, sz1) = file_list[i]
                path2, (sig2, sz2) = file_list[j]
                sim = self.estimate_jaccard_similarity(sig1, sig2)
                if 0.70 <= sim < 1.0:
                    near_dupes.append({
                        "file_a": path1,
                        "file_b": path2,
                        "similarity_score": sim,
                        "recommendation": "Review for version merge or differential archival"
                    })

        return {
            "scanned_files": scanned_count,
            "exact_duplicate_groups": len(exact_dupes),
            "space_reclaimable_bytes": total_reclaimable,
            "exact_duplicates": exact_dupes,
            "near_duplicates": near_dupes
        }
