import os
import zipfile

SKILL_MD = """---
name: vaultsense-ugos
description: Duplicate file discovery, SHA-256 and metadata integrity baseline auditing, and invoice-to-contract tax reconciliation report workflow for UGREEN AI NAS. Use when the user asks to scan a folder for duplicates, verify file checksums or suspicious modifications, extract and reconcile invoices and contracts, or save an audit summary on NAS.
---

# Goal

Deliver an auditable, privacy-preserving storage hygiene, integrity verification, and financial document reconciliation workflow on UGREEN AI NAS (`kimage-planb` full `main-agent` profile) by orchestrating registered UGOS experts across authorized NAS folders:

1. Identify byte-identical duplicate files and summarize reclaimable storage capacity without deleting user data.
2. Audit file metadata, timestamps, sizes, and SHA-256 checksums against user-supplied integrity baselines or designated canary reference files to flag unexpected modifications.
3. Extract structured fields from invoices, receipts, and contracts, detect business-signal duplicate billing, and reconcile invoice totals against contract amounts.
4. Save a verified Markdown audit and tax reconciliation report to an authorized NAS folder, and optionally tag or archive confirmed items only after platform approval.

VaultSense UGOS (`vaultsense-ugos`) is an independent third-party orchestration Skill built for the UGREEN Hackathon 2026 on AI NAS and is not an official UGREEN product. All real NAS operations run exclusively through `delegate` calls to registered child experts with zero undisclosed external network transfers.

# Required input

Collect only the parent-level workflow inputs needed to scope delegation; never pre-collect private CLI flags owned by child experts:

- **Target folder scope** (required): One or more user-authorized NAS folder names or locations to inspect (keep batch scope to the smallest explicit folder supplied by the user).
- **Workflow mode** (optional, defaults to full audit): Duplicate scan, SHA-256 integrity baseline check, invoice-to-contract reconciliation, or combined full audit.
- **Baseline or canary reference list** (optional): Expected SHA-256 digests or canary filenames provided by the user for tamper comparison.
- **Report or archive destination** (optional): User-authorized NAS folder for saving the Markdown audit ledger (`save-text`) or organizing confirmed duplicates/invoices when explicitly requested.

If the target folder scope is missing or ambiguous, ask one concise clarification question before dispatching write-capable or multi-step delegations.

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `file-workflow` → `file-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`

# Workflow

Execute delegations sequentially, passing only verified real results from upstream `completed` steps to downstream steps. Never guess file paths, tag IDs, hashes, or financial amounts.

1. **Step 1 — Read-Only Duplicate & SHA-256 Integrity Audit (`file-agent`)**
   Dispatch `file-agent` to resolve the user-authorized folder scope and perform non-destructive duplicate and integrity inspection:
   `delegate --target file-agent --instruction 'Within the user-authorized NAS folder scope, run read-only duplicate hash scanning via ug-filemgr scan-dedupe and inspect file paths, sizes, modification timestamps, and SHA-256 digests via ug-filesystem find, ls, stat, get-dir-size, and sha256sum; compare any user-supplied baseline hashes or canary filenames to flag unexpected modifications, and return verified duplicate groups, file paths, sizes, timestamps, and checksum anomalies without modifying, moving, or deleting any files.'`
   - **Handoff gate**: Inspect the terminal `delegation_result`. If the scan explicitly reports no results, zero matches, or an empty directory, report that verified empty result accurately and stop dependent document or archival steps unless separate document paths were explicitly supplied.

2. **Step 2 — Structured Invoice Extraction & Contract Reconciliation (`document-agent`)**
   When the user requests financial vaulting or full audit and Step 1 (or explicit user input) provides verified real document paths, dispatch `document-agent`:
   `delegate --target document-agent --instruction 'Using only the verified document paths confirmed in the real upstream result within the authorized folder scope, inspect document metadata and page counts via ug-document metadata, run structured invoice, receipt, and contract extraction with business-signal deduplication enabled via ug-document extract, and reconcile contract totals against invoice amounts via ug-document reconcile and qa; return verified vendor names, tax identifiers, dates, totals, duplicate invoice flags, reconciliation discrepancies, source citations, and coverage details without modifying original files.'`
   - **Handoff gate**: Require `completed` with verified extraction/reconciliation facts before saving a ledger. If no matching invoices or contracts exist (`no results` / `zero matches`), record that fact honestly in the summary without fabricating financial entries.

3. **Step 3 — Markdown Audit & Tax Ledger Persistence (`knowledge-agent`)**
   When the user asks to save the audit or tax reconciliation report to NAS and upstream findings are verified, dispatch `knowledge-agent`:
   `delegate --target knowledge-agent --instruction 'Compile only the verified duplicate groups, SHA-256 integrity findings, extracted invoice records, and contract reconciliation discrepancies from the real upstream results into a structured Markdown audit ledger, and save the report to the user-authorized NAS folder via ug-knowledge save-text after required workflow approval; return the confirmed saved report path and verification status without inventing unverified fields.'`
   - **Verification boundary**: Treat `save-text` completion (`verified`) as file-save confirmation only; it does not establish knowledge search-index readiness (`index-ready`).

4. **Step 4 — Optional Approved Tagging or Archive Organization (`file-agent`)**
   Run this step **only** when the user explicitly requests tagging or moving/copying confirmed items into an archive folder and all target file paths are verified from real upstream results:
   `delegate --target file-agent --instruction 'Run this step only when the user explicitly requested tagging or archive organization and upstream steps returned verified real file paths: apply requested review tags via ug-filemgr tag-add and tag-add-file after gateway approval, or create and execute an approved transfer plan into the user-specified archive folder via file-workflow start, run, or batch-transfer after workflow approval; never delete files automatically and stop immediately if any required path or approval is missing.'`

# Completion and failure

Handle every public delegation state and platform checkpoint strictly according to the Uliya parent result contract:

- `completed`: Verify that `summary` and `result` contain the concrete paths, hashes, or extracted fields required by the current goal and any downstream step. Note that `result: {}` can be valid when verified business text is returned in `summary`, whereas a missing required path or ID halts dependent steps immediately without guessing.
- `failed`: Stop all dependent downstream steps immediately. Report which step and expert (`file-agent`, `document-agent`, or `knowledge-agent`) failed, summarize only confirmed safe error facts, and preserve any already completed read-only findings without claiming overall completion.
- `cancelled`: Report the workflow as incomplete at the cancelled step. Do not automatically switch experts or retry state-changing operations (`save-text`, `tag-add-file`, `batch-transfer`, `run`) that could duplicate effects; explain any potential partial effects before asking whether the user wants a manual retry.
- `waiting_user`: Wait for the platform `ctx.ask` clarification flow to collect the user's answer and resume the same active delegation. Never launch parallel replacement delegations while waiting.
- `waiting_approval`: Wait for platform `gateway` or `workflow` approval via `ctx.ask` and resume the same delegation. Never treat conversational chat agreement as a substitute for platform approval, and inspect the eventual resumed terminal status (`completed`, `failed`, or `cancelled`) rather than assuming approval implies execution success.
- **Empty & partial results**: When a query or scan returns `no results`, `empty result`, or `zero matches`, report that exact outcome and stop without broadening folder scope or substituting unrelated files. For multi-step runs where an earlier step succeeds and a later step stops, report completed, failed/cancelled, waiting, and dependency-blocked steps separately rather than inventing a custom partial status.

# Supporting references

Read these linked package references when progressive detail is needed:

- Read [User Guide & Configuration Template](references/readme-guide.md) for conversational usage examples, target user scenarios, and synthetic input/configuration templates.
- Read [Capability Mapping & Integrity Protocol](references/capability-mapping.md) for the step-by-step CLI Action matrix, approval gates (`none`, `gateway`, `workflow`), and SHA-256 baseline comparison rules.
- Read [Validation Plan & Test Cases](references/validation-plan.md) for local static check verification and Finalist Round 2 test cases on UGREEN AI NAS iDX6011 Pro.
- Read [Disclosures, Licenses & AI Tool Usage](references/disclosures.md) for newly developed Hackathon scope, third-party licenses, zero-external-transfer data flow disclosures, and AI development tool disclosures.

The Skill is complete. You can upload it to [skillhub](https://skills.ugreen.com/skill-hub/publish).
"""

README_GUIDE_MD = """# VaultSense UGOS — User Guide & Configuration Template

## Who This Skill Is For

**VaultSense UGOS** (`vaultsense-ugos`) is designed for UGREEN AI NAS owners—freelancers, independent studios, home-office professionals, and small businesses—who store important project archives, contracts, receipts, and tax invoices on their NAS and want local storage intelligence without uploading private files to external SaaS clouds.

## What Problems It Solves

1. **Duplicate Storage Waste**: Repeated camera imports, copied project folders, and re-downloaded email attachments quietly consume NAS disk space. VaultSense identifies exact hash duplicates (`ug-filemgr` `scan-dedupe`) and flags duplicate invoice/receipt submissions sharing the same billing signals (`ug-document` `extract` with `dedupe=true`).
2. **Silent File Tampering or Accidental Overwrites**: Shared folders can suffer unexpected modifications, renames, or corruption. VaultSense inspects file sizes, modification timestamps (`stat`), and cryptographic SHA-256 digests (`sha256sum`) against user-supplied baselines or designated canary reference files.
3. **Tax-Season Reconciliation Bottlenecks**: Hunting across folders to match PDF/scanned invoices against signed contracts is slow and error-prone. VaultSense extracts structured vendor, tax ID, date, and amount fields (`extract`) and performs deterministic multi-contract vs. invoice reconciliation (`reconcile`), saving a clean Markdown ledger (`save-text`).

## Example Trigger Prompts

- *"Scan my Finance2026 Invoices folder for duplicate files, extract all invoice and contract totals, reconcile any billing mismatches, and save a Markdown tax audit report."*
- *"Check SHA-256 checksums and recent modification timestamps in my StudioArchive CanaryBaseline folder and list any files that changed."*
- *"Find exact duplicate documents in SharedTeam QuarterlyReceipts and, after my approval, tag duplicates with ReviewDuplicate."*

## Configuration & Input Template (Synthetic Placeholders Only)

VaultSense UGOS requires **no external API keys, passwords, or resident daemon config files**. Users may optionally keep a plain Markdown baseline note in their authorized NAS workspace using synthetic placeholders structured like the template below:

```yaml
vaultsense_audit_profile:
  authorized_folder_scope: "PersonalWorkspace/Finance2026"
  audit_mode: "full-audit"
  duplicate_scan_scope: "documents"
  canary_reference_files:
    - filename: "00_canary_budget_reference.pdf"
      expected_sha256: "EXAMPLE_PLACEHOLDER_SHA256_DIGEST_DO_NOT_USE_REAL_SECRETS"
  report_output:
    save_markdown_ledger: true
    destination_folder: "PersonalWorkspace/AuditReports"
    filename_hint: "vaultsense-tax-integrity-audit"
  optional_post_audit_action:
    apply_review_tag: false
    tag_name: "VaultSense-Review"
    archive_folder: "PersonalWorkspace/VerifiedArchive"
```

## Safety & Confirmation Guarantees

- **Read-only first**: Discovery, duplicate scanning, SHA-256 integrity checks, OCR extraction, and contract reconciliation run strictly read-only (`approval=none`).
- **Mandatory platform approval for writes**: Saving a Markdown report (`save-text`), creating or binding tags (`tag-add`, `tag-add-file`), or copying/moving confirmed files (`file-workflow`) always triggers Uliya platform approval (`gateway` or `workflow`).
- **Zero automatic deletion**: VaultSense never deletes user files during duplicate reporting or tax auditing.
"""

CAPABILITY_MAPPING_MD = """# Capability Mapping & Integrity Protocol

## Catalog Alignment Summary

Every operation in `vaultsense-ugos` maps strictly to published capabilities in Uliya Capability Catalog structure version `2.2.0` (`kimage-planb` full `main-agent` profile). Each CLI delegates exclusively to its single catalog-assigned expert agent:

| Workflow Step | CLI Capability | Assigned Expert | Catalog Actions Used | Effect | Approval Gate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1A. Folder & Metadata Discovery | `ug-filesystem` | `file-agent` | `find`, `ls`, `stat`, `get-dir-size` | `read` | `none` |
| 1B. Cryptographic Integrity Check | `ug-filesystem` | `file-agent` | `sha256sum` | `read` | `none` |
| 1C. Hash Duplicate Detection | `ug-filemgr` | `file-agent` | `scan-dedupe`, `tag-list` | `read` | `none` |
| 2A. Document Overview & Pages | `ug-document` | `document-agent` | `metadata` | `read` | `none` |
| 2B. Invoice/Receipt Extraction | `ug-document` | `document-agent` | `extract` (`dedupe=true`) | `read` | `none` |
| 2C. Contract-Invoice Audit | `ug-document` | `document-agent` | `reconcile`, `qa` | `read` | `none` |
| 3. Save Markdown Audit Ledger | `ug-knowledge` | `knowledge-agent` | `save-text` | `state-change` | `workflow` |
| 4A. Review Tag Binding (Optional) | `ug-filemgr` | `file-agent` | `tag-add`, `tag-add-file` | `state-change` | `gateway` |
| 4B. Batch Archive Move/Copy (Optional) | `file-workflow` | `file-agent` | `start`, `run`, `batch-transfer` | `state-change` | `workflow` |

## Integrity & Canary Baseline Protocol

Because Uliya Skills are invocation-scoped Markdown orchestrations (resident background daemons and kernel hooks are prohibited by platform safety standards), VaultSense implements **deterministic on-demand integrity verification**:

1. **Reference Checksum Verification**: When the user supplies expected SHA-256 digests or points to a previously saved Markdown audit ledger, `file-agent` computes current digests via `ug-filesystem` `sha256sum` and compares file size and modification time (`mtime`, `ctime`) via `stat`.
2. **Metadata Anomaly Triage**: Within the bounded target folder, `file-agent` uses `find` and `ls` to identify sudden bursts of recently modified files, zero-byte truncations, or unexpected extension changes on designated canary reference documents.
3. **Non-Destructive Alerting**: Flagged mismatches are reported with exact file paths, observed vs. expected SHA-256 digests, and timestamps so the user can review and approve tagging or isolation without risking automated data loss.

## Upstream-to-Downstream Result Contract

- Downstream delegations consume only verified paths, hashes, and extracted facts returned in a `completed` public `delegation_result`.
- `ug-document` `extract` and `reconcile` never run on guessed paths; if `file-agent` returns zero matching documents, the workflow stops cleanly and reports the empty result.
- `ug-knowledge` `save-text` confirmation (`verified`) confirms file creation on NAS storage only and is never misrepresented as knowledge search-index readiness (`index-ready`).
"""

VALIDATION_PLAN_MD = """# Validation Plan & Test Cases

## Round 1 Static & Contract Verification (Completed)

- **Uliya Static Checker (`check-skill.mjs`, checkFormatVersion `2.0.0`, catalog `2.2.0`)**: Verified package directory structure (`vaultsense-ugos/SKILL.md` + `references/*.md`), frontmatter constraints, `# Generation-time capability evidence` CLI-to-agent ownership mappings, single-quoted `delegate` commands, all five public status handlers (`completed`, `failed`, `cancelled`, `waiting_user`, `waiting_approval`), and security scan compliance (`0` errors, `0` warnings).
- **Capability Boundary Audit**: Confirmed zero unsupported scripts, binaries, manifests, resident daemons, hardcoded paths, or direct host invocations.

## Round 2 Finalist Hardware Validation Plan (UGREEN AI NAS iDX6011 Pro)

During the assigned Finalist remote testing day on the UGREEN AI NAS iDX6011 Pro (64GB), VaultSense UGOS will execute the following structured test suite using synthetic, non-sensitive test files:

### Core Test Case 1 — End-to-End Duplicate Scan + Multi-Invoice Contract Reconciliation
- **Setup**: Upload a synthetic project folder containing 3 byte-identical PDF copies, 4 vendor invoices (including 1 duplicate billing invoice with re-saved filename), and 2 signed service contracts with an intentional amount discrepancy.
- **Trigger**: Ask VaultSense UGOS to run a full duplicate and tax reconciliation audit and save a Markdown ledger.
- **Expected Result**:
  - `file-agent` (`scan-dedupe`, `get-dir-size`) groups the 3 identical PDFs without deleting any file.
  - `document-agent` (`metadata`, `extract`, `reconcile`) extracts vendor/date/tax/amount fields, flags the duplicate invoice signal, and calculates the exact contract-vs-invoice variance with source citations.
  - Platform triggers `waiting_approval` (`workflow`) before `knowledge-agent` (`save-text`) writes the Markdown ledger; upon approval, `completed` returns the verified report path.

### Core Test Case 2 — Canary SHA-256 Baseline Mismatch & Approved Review Tagging
- **Setup**: Seed 2 synthetic canary reference documents with recorded SHA-256 digests, modify 1 file's contents to simulate unauthorized alteration, and request an integrity check plus `VaultSense-Review` tagging on altered files.
- **Expected Result**:
  - `file-agent` (`stat`, `sha256sum`) detects the exact SHA-256 digest and `mtime` mismatch on the altered file while confirming the untouched file matches baseline.
  - Platform triggers `waiting_approval` (`gateway`) before `tag-add` / `tag-add-file`; after approval, only the verified altered file receives the review tag.

### Edge Case — Empty Folder, Unreadable Scan, or Rejected Approval
- **Setup**: Run against (a) an empty authorized folder, (b) a corrupted/blank image PDF, and (c) an archive move request where platform approval is declined.
- **Expected Result**:
  - Empty folder reports `no results` / `zero matches` immediately and halts downstream steps without broadening search scope.
  - Unreadable document reports accurate partial coverage warnings from `document-agent` without inventing numbers.
  - Declined `waiting_approval` terminates the write step cleanly (`failed` or `cancelled` per resumed platform status) while preserving prior read-only audit findings.
"""

DISCLOSURES_MD = """# Disclosures, Licenses & AI Tool Usage

## 1. Independent Entry & Principal Newly Developed Functionality

- **Entrant**: Khanhtnq (Individual Entrant)
- **Project**: VaultSense UGOS (`vaultsense-ugos`)
- **Non-Affiliation Notice**: VaultSense UGOS is an independent third-party participant submission created for the UGREEN Hackathon 2026 on AI NAS and is not an official, certified, or UGREEN-authored product.
- **Newly Developed Functionality (October–November 2026)**: Designed and authored from scratch during the Hackathon Period, including the multi-expert orchestration workflow (`SKILL.md`), four-stage handoff and approval state machine across `file-agent`, `document-agent`, and `knowledge-agent`, on-demand SHA-256 canary/baseline verification protocol, invoice-to-contract tax reconciliation ledger structure, and supporting reference documentation (`references/*.md`). No pre-existing Skill or prior submission material was reused.

## 2. Third-Party Components, Specifications & Open-Source Licenses

The submitted Uliya Skill package (`vaultsense-ugos`) consists solely of original UTF-8 Markdown orchestration files (`SKILL.md` and `references/*.md`) licensed under the **MIT License** (`Copyright (c) 2026 Khanhtnq`) and bundles zero third-party binaries, scripts, or proprietary assets. Development and local verification used the following authorized tools and open-source packages:

| Component / Tool | Source / Author | Version | Applicable License | Role in Development |
| :--- | :--- | :--- | :--- | :--- |
| UGOS Skill Creation Tool (`uliya-skill-kit`) | America Ugreen Limited (`ai.ugreen.com/pages/hackathon-starter-kit`) | `0.7.7-en` (Catalog `2.2.0`) | UGREEN SkillHub User Agreement & Starter Kit Terms | Official capability catalog reference and `check-skill.mjs` static validation |
| Node.js Runtime | OpenJS Foundation (`nodejs.org`) | `v20+` | MIT License | Running the official read-only `check-skill.mjs` static validator locally |
| Python & ReportLab (Proposal PDF build only, excluded from Skill ZIP) | Python Software Foundation / ReportLab Inc. (`pypi.org/project/reportlab`) | Python `3.11` / ReportLab `4.x` | PSF License / BSD-3-Clause License | Formatting the separate Round 1 Project Proposal PDF |

## 3. External Services, Permissions & Data Flow Disclosure

- **External Network Connections**: **None.** `vaultsense-ugos` initiates zero connections to external third-party APIs, webhooks, or cloud servers.
- **Data Flow**: All file discovery, SHA-256 hashing, OCR/VLM document extraction, contract reconciliation, tagging, archival transfers, and Markdown report saving execute within the UGREEN AI NAS / Uliya runtime via registered experts (`file-agent`, `document-agent`, `knowledge-agent`) operating solely on paths explicitly authorized by the user.
- **Permissions**: Read-only actions (`find`, `ls`, `stat`, `get-dir-size`, `sha256sum`, `scan-dedupe`, `metadata`, `extract`, `reconcile`, `qa`) require read access to the user-specified NAS folder. State-changing actions (`save-text`, `tag-add`, `tag-add-file`, `file-workflow`) execute only when requested by the user and approved through Uliya `gateway` or `workflow` checkpoints.

## 4. AI Tools Disclosure

In accordance with the Hackathon Rules and Resources FAQ, the following AI assistants were used as development aids:

- **Claude / AI Coding Assistant (IDE workflow)**: Used to cross-check Uliya Capability Catalog `2.2.0` CLI/Action schemas, verify `check-skill.mjs` diagnostic rules, refine grammar and conciseness, and format documentation tables. Core workflow architecture, problem selection, capability combination, and validation design were directed and verified by the Entrant.

## 5. Package License (MIT License)

Copyright (c) 2026 Khanhtnq. Permission is hereby granted, free of charge, to any person obtaining a copy of this Skill and associated documentation files to deal in the files without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, subject to inclusion of this copyright and permission notice. Provided "AS IS", without warranty of any kind.
"""

def build_v2_skill():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pkg_root = os.path.join(workspace, "skill_package", "vaultsense-ugos")
    refs_dir = os.path.join(pkg_root, "references")
    os.makedirs(refs_dir, exist_ok=True)

    files_to_write = {
        os.path.join(pkg_root, "SKILL.md"): SKILL_MD.lstrip(),
        os.path.join(refs_dir, "readme-guide.md"): README_GUIDE_MD.lstrip(),
        os.path.join(refs_dir, "capability-mapping.md"): CAPABILITY_MAPPING_MD.lstrip(),
        os.path.join(refs_dir, "validation-plan.md"): VALIDATION_PLAN_MD.lstrip(),
        os.path.join(refs_dir, "disclosures.md"): DISCLOSURES_MD.lstrip(),
    }

    for path, content in files_to_write.items():
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

    # Also update root SKILL.md and root references/ in workspace for repo consistency
    root_refs = os.path.join(workspace, "references")
    os.makedirs(root_refs, exist_ok=True)
    with open(os.path.join(workspace, "SKILL.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(SKILL_MD.lstrip())
    for name in ["readme-guide.md", "capability-mapping.md", "validation-plan.md", "disclosures.md"]:
        src_p = os.path.join(refs_dir, name)
        dst_p = os.path.join(root_refs, name)
        with open(dst_p, "w", encoding="utf-8", newline="\n") as f:
            f.write(open(src_p, encoding="utf-8").read())

    dist_dir = os.path.join(workspace, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    zip_v2_path = os.path.join(dist_dir, "ugreen_vaultsense_skill_v2.zip")

    with zipfile.ZipFile(zip_v2_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(pkg_root):
            dirs.sort()
            for file in sorted(files):
                full_p = os.path.join(root, file)
                arc_p = os.path.relpath(full_p, os.path.join(workspace, "skill_package")).replace("\\", "/")
                zf.write(full_p, arcname=arc_p)

    print(f"Built {zip_v2_path} ({os.path.getsize(zip_v2_path)} bytes)")
    with zipfile.ZipFile(zip_v2_path, "r") as zf:
        for info in zf.infolist():
            print(f"  {info.filename} -> {info.file_size} bytes")

if __name__ == "__main__":
    build_v2_skill()
