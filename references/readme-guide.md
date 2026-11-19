# VaultSense UGOS — User Guide & Configuration Template

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
