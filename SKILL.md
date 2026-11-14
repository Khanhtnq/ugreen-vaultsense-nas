---
name: "VaultSense UGOS"
id: "com.ugreen.skill.vaultsense"
version: "1.0.0"
author: "Khanhtnq"
license: "MIT"
description: "Zero-Cloud Semantic Deduplicator, Entropy Ransomware Canary & Invoice Tax Vault Skill for UGREEN AI NAS"
scopes:
  - ugos.nas.files.read
  - ugos.nas.files.dedup
  - ugos.nas.security.canary
  - ugos.nas.knowledge.invoice
hardware:
  cpu_architecture: ["x86_64", "aarch64"]
  npu_support: true
  min_memory: "1GB"
---

# VaultSense UGOS — Zero-Cloud Storage Intelligence Skill

**VaultSense** is an autonomous, 100% on-premises edge AI skill architected natively for the **UGREEN AI NAS (UGOS)** ecosystem. It addresses three of the most pressing pain points for home lab, prosumer, and SMB NAS operators:

1. **Zero-Cloud Semantic Deduplicator**: Multi-tier duplicate detection combining fast cryptographic hashing (BLAKE3/SHA-256) with rolling block chunking and MinHash semantic fingerprinting. Identifies identical files and visually near-identical photo bursts, multi-resolution video backups, and versioned documents across SMB/NFS shares without sending a single byte to external clouds.
2. **Real-Time Shannon Entropy Ransomware Canary**: Continuous filesystem entropy monitor and honeypot canary bait system. Detects anomalous mass encryption events (sudden spikes in byte entropy above 7.85 bits/byte paired with rapid extension mutation) and halts suspicious processes while isolating affected storage volumes.
3. **Automated Invoice & Tax Document Vault**: Local OCR and regex-heuristic parser that automatically indexes invoices, receipts, and bank statements, extracts VAT numbers, currency totals, invoice numbers, and vendor names, and tags documents into tax-ready folders.

## Architecture

```
+-------------------------------------------------------------------------+
|                           UGREEN AI NAS (UGOS)                          |
|                                                                         |
|  +--------------------+   +-----------------------+   +---------------+ |
|  | Local SMB/NFS Pools|   |   UGOS Event Bus      |   | NPU Accel.    | |
|  +---------+----------+   +-----------+-----------+   +-------+-------+ |
|            |                          |                       |         |
|            +--------------------------+-----------------------+         |
|                                       v                                 |
|                       +-------------------------------+                 |
|                       |  com.ugreen.skill.vaultsense  |                 |
|                       |                               |                 |
|                       |  [1] Semantic Deduplicator    |                 |
|                       |  [2] Entropy Ransomware Sentry|                 |
|                       |  [3] Invoice Tax Parser       |                 |
|                       |  [4] FastAPI Microservice     |                 |
|                       +---------------+---------------+                 |
|                                       |                                 |
|                                       v                                 |
|                 +-------------------------------------------+           |
|                 |  Interactive Web Dashboard (Local Port)   |           |
|                 +-------------------------------------------+           |
+-------------------------------------------------------------------------+
```

## Quick Start (Pre-test Local Validation)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest -v tests/

# 3. Launch the Skill daemon
uvicorn vaultsense.api:app --host 0.0.0.0 --port 8443
```

Navigate to `http://localhost:8443/docs` or open `docs/index.html` to interact with the responsive dashboard.
