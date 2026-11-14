# VaultSense UGOS — Devpost Submission Details

**Hackathon**: UGREEN Hackathon 2026 on AI NAS ($46,000 USD Cash Prize Pool)  
**Round**: Round 1 (Local Pre-test & Technical Proposal)  
**Project Title**: VaultSense UGOS — Zero-Cloud Semantic Deduplicator, Entropy Ransomware Canary & Invoice Tax Vault Skill  
**Author**: Khanhtnq (`218711032+Khanhtnq@users.noreply.github.com`)  
**Repository**: `e:\BOUTY ARGON\workspaces\ugreen_nas_skill_46k`  

---

## Pitch & Inspiration
Modern NAS users buy network-attached storage because they demand **100% data sovereignty and privacy**. But as NAS volumes swell into tens of terabytes, users face two compounding nightmares:
1. Massive storage waste from redundant burst photo backups, duplicate video edits, and disorganized documents.
2. Ransomware operators targeting SMB/NFS storage pools with silent encryption attacks.
3. The daunting chore of gathering business receipts and VAT invoices scattered across folders for annual tax filing.

Most AI tools require streaming personal files to public clouds for processing. **VaultSense UGOS** runs entirely on the UGREEN AI NAS local processor and NPU, offering zero-cloud intelligence that preserves privacy.

---

## What It Does
- **Zero-Cloud Semantic Deduplicator**: Combines cryptographic SHA-256 chunk hashing with MinHash Jaccard token analysis to spot exact duplicates and near-identical document bursts across NAS volumes.
- **Shannon Entropy Ransomware Canary**: Calculates mathematical byte entropy ($H = -\sum p_i \log_2 p_i$) on storage pools and arms hidden honey-canary bait files. If entropy surges past 7.85 bits/byte on non-compressed documents, it alerts the admin and halts rogue processes.
- **Invoice & Tax Vault**: Parses unstructured documents, detects VAT IDs, currencies, and invoice line items, and categorizes deductible expenses.

---

## Technical Feasibility & Deliverables
1. **Pre-test Skill Package**: Packaged in `dist/ugreen_vaultsense_skill.zip` adhering strictly to UGREEN Skill Developer Package guidelines (`manifest.json` schema v2, `SKILL.md` frontmatter, Docker Compose, FastAPI).
2. **Technical Proposal PDF**: Packaged in `dist/UGREEN_VaultSense_Proposal.pdf` detailing the architecture, threat models, and Round 2 plan on physical hardware (`iDX6011 Pro`).
3. **Automated Verification**: Complete `pytest` test suite with 10 passing unit tests.
4. **Interactive Dashboard**: Zero-dependency, responsive local UI at `docs/index.html`.
