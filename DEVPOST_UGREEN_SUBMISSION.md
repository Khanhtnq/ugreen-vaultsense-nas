# VaultSense UGOS — Devpost Submission Details

## Devpost Form Metadata
- **Hackathon**: UGREEN Hackathon 2026 on AI NAS (`https://ugreenhackathon.devpost.com/`, $46,000 USD Prize Pool)
- **Project Name**: `VaultSense UGOS`
- **Elevator Pitch (166 chars)**: `Zero-cloud UGREEN AI NAS skill combining MinHash semantic deduplication, Shannon entropy ransomware canary protection, and automated local VAT/tax invoice extraction.`
- **Track / Prize Category**: `Workflow (Automate Your Workflow)` & `Innovation` (Round 1 Pre-test & Proposal; Eligible for Gold/Silver/Bronze & Most Creative Skills Awards)
- **Built With**: `python`, `fastapi`, `docker`, `ugos`, `minhash`, `sha-256`, `edge-ai`, `html5`, `javascript`, `pytest`
- **GitHub Repository URL**: `https://github.com/Khanhtnq/ugreen-vaultsense-nas`
- **Try It Out Links**:
  - `https://khanhtnq.github.io/ugreen-vaultsense-nas/`
  - `https://github.com/Khanhtnq/ugreen-vaultsense-nas`
- **File Attachments**:
  - `dist/ugreen_vaultsense_skill.zip` (UGREEN Pre-test Skill Developer Package v2)
  - `dist/UGREEN_VaultSense_Proposal.pdf` (Technical Architecture & iDX6011 Pro Round 2 Proposal)
- **YouTube Title**: `VaultSense UGOS — Zero-Cloud AI NAS Deduplicator, Ransomware Canary & Tax Vault (1080p Demo)`
- **YouTube Description**:
  ```text
  VaultSense UGOS — Official Demo for the UGREEN Hackathon 2026 on AI NAS ($46,000 Prize Pool).
  100% On-Premises Storage Intelligence Skill for UGREEN UGOS Pro / iDX6011 Pro:
  1. Zero-Cloud Semantic Deduplicator (Content-Defined Chunking + SHA-256 + MinHash Jaccard similarity)
  2. Shannon Entropy Ransomware Canary (Real-time H > 7.85 bits/byte detection + honeypot bait traps)
  3. Automated Local Invoice & VAT Tax Vault (Zero-egress receipt & tax categorization)

  Live Interactive Demo: https://khanhtnq.github.io/ugreen-vaultsense-nas/
  Open-Source Repository: https://github.com/Khanhtnq/ugreen-vaultsense-nas
  ```

---

## About the Project (Markdown Story)

### Inspiration
Modern NAS owners invest in network-attached storage because they demand **100% data sovereignty and zero cloud surveillance**. Yet as personal and SMB NAS volumes scale into tens of terabytes, users face three compounding operational headaches:
1. **Silent Storage Bloat**: Redundant burst photo backups, near-duplicate video renders, and multi-version office documents quietly consume expensive NVMe and HDD RAID arrays.
2. **Ransomware Encryption Attacks**: Threat actors increasingly target mounted SMB/NFS network shares, silently encrypting family archives and business records before standard antivirus tools react.
3. **Tax-Season Chaos**: Freelancers and small businesses waste days hunting down scattered PDF receipts and VAT invoices across shared folders, yet refuse to upload confidential financial statements to third-party cloud SaaS platforms.

**VaultSense UGOS** solves all three problems directly on the **UGREEN AI NAS** local CPU/NPU with **zero external cloud egress**.

### What It Does
- **Zero-Cloud Semantic Deduplicator**: Combines deterministic SHA-256 cryptographic hashing with 64-permutation MinHash Jaccard token similarity to pinpoint both byte-identical duplicates and near-identical document revisions across UGOS volumes.
- **Shannon Entropy Ransomware Canary**: Continuously computes mathematical byte entropy ($H = -\sum p_i \log_2 p_i$) across watched SMB/NFS shares and deploys hidden `.canary_traps` bait files. When non-compressed files surge past `7.85 bits/byte` or a canary trap is touched, VaultSense immediately raises a critical incident alert to isolate the rogue client.
- **Automated Invoice & Tax Vault**: Locally parses unstructured receipts and invoices to extract invoice IDs, dates, VAT registration numbers, currency totals, and tax-deductible expense categories without a single byte leaving the LAN.

### How We Built It
- **UGOS Skill Architecture**: Packaged strictly to the UGREEN Skill Developer Package v2 specification (`manifest.json`, `SKILL.md` frontmatter, `Dockerfile`, and `docker-compose.yml` container orchestration).
- **FastAPI Microservice (`vaultsense/`)**: Modular Python 3.11 engine exposing clean REST endpoints (`/health`, `/scan/dedup`, `/scan/canary`, `/scan/invoices`) for seamless UGOS Control Center integration.
- **Zero-Dependency Web Console (`docs/index.html`)**: Responsive dark-mode interactive dashboard enabling real-time deduplication previews, live entropy gauges, and one-click CSV/JSON tax exports.
- **Automated Verification (`tests/`)**: Comprehensive `pytest` test suite (`10/10` passing unit and API integration tests).

### Challenges We Ran Into
- **Distinguishing Legitimate Compressed Archives from Ciphertext**: Standard `.zip`, `.mp4`, and `.jpg` files naturally exhibit high byte entropy (`> 7.9 bits/byte`). We engineered magic-byte header inspection alongside file-extension whitelisting and dedicated honeypot canary files to eliminate false positives while maintaining sub-millisecond detection on encrypted office documents.
- **Low-Memory Footprint for Multi-Terabyte Pools**: Streaming 64KB chunk windows and compact MinHash signatures keeps container RAM usage well below `256 MB`, ensuring smooth coexistence with UGOS media transcoding services.

### Accomplishments That We're Proud Of
- Delivering a unified **3-in-1 privacy-first storage workflow skill** with **0 external API keys** and **0 cloud dependencies**.
- Achieving `100%` pass rate across all unit and REST API verification suites alongside a ready-to-deploy UGOS Docker skill bundle and multi-page hardware roadmap PDF.

### What We Learned
- Designing containerized edge AI workflows specifically tailored for NAS I/O characteristics, least-privilege volume mounts, and deterministic local inference.

### What's Next for VaultSense UGOS (Round 2 Hardware Plan on UGREEN iDX6011 Pro)
- **Intel Core Ultra NPU Acceleration**: Offload local multimodal embeddings (CLIP / ONNX Runtime OpenVINO EP) onto the iDX6011 Pro NPU for perceptual photo/video frame deduplication.
- **UGOS Snapshot Rollback Hook**: Trigger instant Btrfs/ZFS read-only volume snapshots the millisecond a Shannon entropy canary alert fires.
