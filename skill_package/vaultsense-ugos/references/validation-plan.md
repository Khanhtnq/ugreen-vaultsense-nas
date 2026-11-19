# Validation Plan & Test Cases

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
