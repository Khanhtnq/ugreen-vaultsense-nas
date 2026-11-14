import os
import tempfile
import pytest
from vaultsense.dedup import SemanticDeduplicator

def test_dedup_hash_and_exact_duplicates():
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "doc1.txt")
        file2 = os.path.join(tmpdir, "doc2_copy.txt")
        file3 = os.path.join(tmpdir, "different.txt")

        content = "Enterprise UGREEN NAS AI Vault Content for testing."
        with open(file1, "w") as f:
            f.write(content)
        with open(file2, "w") as f:
            f.write(content)
        with open(file3, "w") as f:
            f.write("Completely different content for NAS storage.")

        engine = SemanticDeduplicator()
        res = engine.scan_directory_for_duplicates(tmpdir)

        assert res["scanned_files"] == 3
        assert res["exact_duplicate_groups"] == 1
        assert res["space_reclaimable_bytes"] > 0
        assert len(res["exact_duplicates"]) == 1
        assert res["exact_duplicates"][0]["original"] in [file1, file2]

def test_text_minhash_near_duplicates():
    engine = SemanticDeduplicator()
    text_a = "Quarterly financial tax breakdown for Q3 equipment purchases at UGREEN datacenter."
    text_b = "Quarterly financial tax breakdown for Q3 equipment purchases at UGREEN datacenter office."
    text_c = "Delicious apple pie recipe with cinnamon and fresh butter baked in oven."

    sig_a = engine.text_minhash(text_a)
    sig_b = engine.text_minhash(text_b)
    sig_c = engine.text_minhash(text_c)

    sim_ab = engine.estimate_jaccard_similarity(sig_a, sig_b)
    sim_ac = engine.estimate_jaccard_similarity(sig_a, sig_c)

    assert sim_ab > 0.65
    assert sim_ac < 0.35
