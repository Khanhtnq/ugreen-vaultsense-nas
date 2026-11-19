---
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
