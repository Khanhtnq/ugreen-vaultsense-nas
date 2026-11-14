import os
import tempfile
import pytest
from vaultsense.canary import EntropyRansomwareCanary

def test_shannon_entropy_calculation():
    # Constant data has 0 entropy
    zero_entropy = b"A" * 1024
    assert EntropyRansomwareCanary.calculate_shannon_entropy(zero_entropy) == 0.0

    # Low entropy typical English prose (approx 3.0 to 4.5)
    prose = b"The quick brown fox jumps over the lazy dog repeatedly in the afternoon sun." * 20
    prose_entropy = EntropyRansomwareCanary.calculate_shannon_entropy(prose)
    assert 3.0 <= prose_entropy <= 5.0

    # Pseudo-random / encrypted data has high entropy close to 8.0
    random_bytes = os.urandom(4096)
    rand_entropy = EntropyRansomwareCanary.calculate_shannon_entropy(random_bytes)
    assert rand_entropy > 7.7

def test_canary_deployment_and_detection():
    with tempfile.TemporaryDirectory() as tmpdir:
        guard = EntropyRansomwareCanary(canary_dir=tmpdir, threshold=7.80)
        deployed = guard.deploy_canaries(count=3)
        assert len(deployed) == 3

        # Check initial healthy state
        status = guard.check_canaries()
        assert status["status"] == "HEALTHY"
        assert status["compromised_count"] == 0

        # Simulate ransomware encrypting one of the canary files
        target = deployed[0]
        with open(target, "wb") as f:
            f.write(os.urandom(8192))

        # Check detection
        status_after = guard.check_canaries()
        assert status_after["status"] == "THREAT_DETECTED"
        assert status_after["compromised_count"] == 1
        assert len(status_after["alerts"]) == 1
