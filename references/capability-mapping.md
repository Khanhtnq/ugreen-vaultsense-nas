# Capability Mapping & Integrity Protocol

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
