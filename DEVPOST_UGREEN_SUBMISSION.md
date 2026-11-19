# VaultSense UGOS (`vaultsense-ugos`) — Devpost Round 1 Submission Details (v2 Official-Rules Compliant)

## Devpost Form Metadata
- **Hackathon**: UGREEN Hackathon 2026 on AI NAS (`https://ugreenhackathon.devpost.com/`, $46,000 USD Prize Pool)
- **Project Name**: `VaultSense UGOS`
- **Skill Name / Slug**: `vaultsense-ugos`
- **Elevator Pitch (178 chars)**: `Uliya AI NAS orchestration Skill unifying duplicate discovery, on-demand SHA-256 canary baseline auditing, and local invoice-to-contract tax reconciliation on UGREEN UGOS.`
- **Track / Prize Category**: `Automate Your Workflow` (Eligible for Gold/Silver/Bronze & Most Creative Skills Awards)
- **Built With**: `ugos`, `uliya`, `markdown`, `ai-agents`, `ocr`, `vlm`, `sha-256`, `nodejs`, `python`
- **File Attachments (Round 1 Required Deliverables)**:
  - **Field 1 (`Pre-test Skill Package (ZIP)`)**: `dist/ugreen_vaultsense_skill_v2.zip` (`vaultsense-ugos/SKILL.md` + 4 linked `references/*.md` files — passes official `check-skill.mjs` v2.0.0 / Catalog `2.2.0` with `status: "static-pass"`, `0` errors, `0` warnings)
  - **Field 4 (`Upload your PDF`)**: `dist/UGREEN_VaultSense_Proposal_v2.pdf` (Answers all 10 Official Rules questions in **398 substantive English words** `<= 500` limit + Page 2 Entrant Consent Declaration, Electronic Signature `/s/ Khanhtnq`, Third-Party Licenses, Data Flow & AI Tool Disclosures)

---

## About the Project (Devpost Markdown Story — 100% Aligned with Uliya Skill Package)

### Inspiration
NAS owners choose on-premises storage for **privacy and data control**, yet day-to-day folder growth introduces three recurring workflow bottlenecks for freelancers, creative studios, and small businesses:
1. **Silent Duplicate Bloat**: Re-downloaded attachments, copied project deliverables, and re-scanned invoices quietly waste NAS capacity.
2. **Undetected Shared-Folder Tampering**: Accidental overwrites or unauthorized edits in sensitive folders often go unnoticed until an archive is needed.
3. **Tax-Season Reconciliation Friction**: Matching PDF/scanned vendor invoices against signed contracts takes hours of manual work, while uploading private financial records to external cloud bookkeeping bots defeats the purpose of owning a NAS.

**VaultSense UGOS (`vaultsense-ugos`)** solves all three workflows natively through the **Uliya Skill Development Standard** on **UGREEN AI NAS (UGOS)**—with zero external cloud transfers and zero automatic file deletion.

### What It Does
VaultSense UGOS is an invocation-scoped Uliya orchestration Skill (`kimage-planb` full `main-agent` profile) that coordinates three registered UGOS experts (`file-agent`, `document-agent`, and `knowledge-agent`) across five published CLI capabilities:
- **Exact & Business-Signal Deduplication**: Uses `ug-filemgr` (`scan-dedupe`) via `file-agent` to group byte-identical files by cryptographic hash and `ug-document` (`extract` with `dedupe=true`) via `document-agent` to flag duplicate invoices sharing identical billing signals.
- **On-Demand SHA-256 & Metadata Canary Baseline Audit**: Uses `ug-filesystem` (`find`, `ls`, `stat`, `get-dir-size`, `sha256sum`) via `file-agent` to verify file digests, sizes, and modification timestamps against user-supplied baselines or designated canary reference files.
- **Structured Invoice-to-Contract Tax Reconciliation**: Uses `ug-document` (`metadata`, `extract`, `reconcile`, `qa`) via `document-agent` to extract vendor names, tax IDs, dates, and totals and deterministically reconcile multi-contract sums against invoice amounts.
- **Approval-Gated Markdown Audit Ledger & Organization**: Saves verified audit and tax reconciliation reports via `ug-knowledge` (`save-text`, `workflow` approval) and optionally applies review tags (`ug-filemgr` `tag-add` / `tag-add-file`, `gateway` approval) or organizes confirmed files (`file-workflow` `start`, `run`, `batch-transfer`, `workflow` approval).

### How We Built It
- **Strict Uliya Skill Standard Architecture**: Engineered around a clean `SKILL.md` entry point and four progressive-disclosure reference guides (`references/readme-guide.md`, `references/capability-mapping.md`, `references/validation-plan.md`, and `references/disclosures.md`), containing zero prohibited scripts, manifests, resident daemons, or binaries.
- **Deterministic Upstream-to-Downstream Handoffs**: Every downstream `delegate` consumes only verified `completed` business facts while explicitly handling `failed`, `cancelled`, `waiting_user`, `waiting_approval`, empty-match (`no results` / `zero matches`), and partial-completion boundaries.
- **Verified with Official UGOS Skill Creation Tool (`uliya-skill-kit` `0.7.7-en`)**: Validated directly against `scripts/check-skill.mjs` (Catalog `2.2.0`) achieving `status: "static-pass"` with `0` errors and `0` warnings.

### Challenges We Ran Into
- **Respecting Invocation-Scoped Safety Boundaries**: Because Uliya Skills prohibit resident background daemons, custom scripts, and direct host file access, we redesigned integrity monitoring into an on-demand cryptographic baseline protocol combining `ug-filesystem` `sha256sum` and `stat` with saved Markdown baseline ledgers.
- **Separating Save Verification from Index Readiness**: In Uliya's knowledge contract, `save-text` completion confirms file persistence (`verified`) rather than search-index readiness (`index-ready`); our workflow passes verified file paths directly rather than assuming immediate index availability.

### Accomplishments That We're Proud Of
- Achieving a clean **`static-pass` (`0` errors, `0` warnings)** on the official Uliya `check-skill.mjs` validator across all 5 Markdown package files.
- Combining storage hygiene, cryptographic integrity verification, and deterministic contract-vs-invoice tax reconciliation in one cohesive, human-in-the-loop NAS workflow with **0 external runtime dependencies**.

### What's Next for VaultSense UGOS (Round 2 Validation on UGREEN AI NAS iDX6011 Pro)
- Execute end-to-end live benchmarking on the assigned **UGREEN AI NAS iDX6011 Pro (64GB)** across mixed duplicate/invoice/contract datasets, `ctx.ask` gateway/workflow approval resume cycles, and low-resolution scanned receipt edge cases.
