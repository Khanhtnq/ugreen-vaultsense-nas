# VaultSense UGOS — Zero-Cloud Storage Intelligence Skill for UGREEN AI NAS

[![UGOS Skill](https://img.shields.io/badge/UGOS-Skill%20v1.0.0-10b981.svg)](https://ugreenhackathon.devpost.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/tests-10%20passed-brightgreen.svg)](tests/)

VaultSense is an enterprise-grade, edge AI skill architected natively for the **UGREEN AI NAS (UGOS)** ecosystem. It delivers three zero-cloud storage capabilities without any external cloud egress:

1. **Zero-Cloud Semantic Deduplicator**: Content-Defined Chunking (CDC) + SHA-256 exact match + MinHash Jaccard token similarity for duplicate burst photos, videos, and multi-version documents across SMB/NFS shares.
2. **Shannon Entropy Ransomware Canary**: Real-time entropy monitor ($H = -\sum p \log_2 p$) that watches file changes and honeypot canary bait files, sounding an alert and halting processes if byte entropy exceeds 7.85 bits/byte on standard documents.
3. **Automated Invoice & Tax Vault**: Local OCR & regex NER parser that extracts VAT numbers, currency totals, invoice IDs, and tags expenses into tax-ready categories.

---

## 🛠️ Repository Structure

```
ugreen_nas_skill_46k/
├── manifest.json                  # Official UGREEN Skill Hub Manifest
├── SKILL.md                       # Skill specification with frontmatter metadata
├── docker-compose.yml             # UGOS Container orchestration
├── Dockerfile                     # Lightweight container image definition
├── requirements.txt               # Python dependencies
├── vaultsense/                    # Core Python Engine
│   ├── api.py                     # FastAPI REST microservice
│   ├── config.py                  # UGOS configuration
│   ├── dedup.py                   # Semantic deduplication & MinHash
│   ├── canary.py                  # Shannon entropy & honeypot guard
│   └── invoice_vault.py           # Local invoice/tax parser
├── tests/                         # Pytest automated test suite (10/10 PASS)
│   ├── test_api.py
│   ├── test_canary.py
│   ├── test_dedup.py
│   └── test_invoice_vault.py
├── docs/                          # Interactive Local Web Dashboard
│   └── index.html
├── dist/                          # Packaged deliverables
│   ├── ugreen_vaultsense_skill.zip # Pre-test Skill Package for Round 1
│   └── UGREEN_VaultSense_Proposal.pdf # Multi-page technical proposal PDF
└── DEVPOST_UGREEN_SUBMISSION.md   # Official Devpost submission copy
```

---

## 🚀 Quick Start & Local Pre-Test

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the test suite
pytest -v tests/

# 3. Launch the API server
uvicorn vaultsense.api:app --host 0.0.0.0 --port 8443

# 4. Open the Web Dashboard
# Open docs/index.html in any modern browser
```
