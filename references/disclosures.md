# Disclosures, Licenses & AI Tool Usage

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
