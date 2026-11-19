import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

QUESTIONS_AND_ANSWERS = [
    (
        "1. One sentence: What does the Skill do?",
        "VaultSense UGOS orchestrates UGREEN AI NAS file, document, and knowledge experts to find duplicate files, verify SHA-256 integrity baselines on sensitive folders, reconcile invoices against contracts, and save auditable tax reports locally."
    ),
    (
        "2. Who is the target user and problem?",
        "Freelancers, studios, and small businesses storing archives and tax records on NAS face duplicate storage bloat, undetected shared-folder tampering, and manual invoice matching—yet refuse to upload private financial files to external cloud AI services."
    ),
    (
        "3. What is your proposed solution?",
        "VaultSense UGOS (vaultsense-ugos) is a Uliya orchestration Skill unifying read-only hash deduplication, on-demand SHA-256 and timestamp canary baseline auditing, invoice-to-contract reconciliation, and approval-gated Markdown ledger saving and archive organization on UGREEN AI NAS."
    ),
    (
        "4. What is the Core User Flow?",
        "The user specifies an authorized NAS folder and audit goal; file-agent runs read-only duplicate and SHA-256 checks; document-agent extracts invoices and reconciles contracts; knowledge-agent saves a Markdown ledger; optionally file-agent tags or archives verified files after platform approval."
    ),
    (
        "5. What substantive difference does your idea offer compared with existing tools or conventional AI solutions?",
        "Cloud bookkeeping bots export private PDFs off-device while basic deduplicators match raw hashes only; VaultSense stays on-premises, combines hash deduplication with invoice business-signal deduplication, verifies SHA-256 tamper baselines, and requires platform approval before writes without automatic deletion."
    ),
    (
        "6. Which UGREEN AI NAS capabilities will be used, and at which step in the workflow?",
        "Step 1: ug-filesystem (find, ls, stat, get-dir-size, sha256sum) and ug-filemgr (scan-dedupe). Step 2: ug-document (metadata, extract, reconcile, qa). Step 3: ug-knowledge (save-text). Optional Step 4: ug-filemgr (tag-add, tag-add-file) and file-workflow (start, run, batch-transfer)."
    ),
    (
        "7. What was your technical approach?",
        "Targeting kimage-planb full main-agent, SKILL.md collects folder scope, audit mode, and optional baseline or destination inputs, delegating sequentially to file-agent, document-agent, and knowledge-agent. Downstream steps require verified completed outputs while handling failed, cancelled, waiting_user, and waiting_approval. Reads need no approval; tagging uses gateway approval; saving ledgers and transfers require workflow approval using local NAS OCR/VLM/LLM with zero external transfers."
    ),
    (
        "8. What is the current development status?",
        "Implemented: Uliya-compliant SKILL.md, four linked references guides, five-CLI orchestration contract, and check-skill.mjs verification (static-pass, zero errors, zero warnings). Pending Finalist validation: live execution, ctx.ask approval resume flows, and OCR/VLM benchmarking on UGREEN AI NAS iDX6011 Pro."
    ),
    (
        "9. What is your final validation plan?",
        "Core Test 1 audits duplicate PDFs, invoices, and contracts to verify scan-dedupe, extract, reconcile discrepancy math, and save-text ledger output. Core Test 2 alters one seeded canary file to verify sha256sum mismatch detection and gateway-approved tagging. Edge Case tests an empty folder and rejected approval, confirming clean halt without guessed paths or file deletion."
    ),
    (
        "10. Are there any known limitations of your Project?",
        "Uliya Skills are invocation-scoped without resident daemons or kernel hooks, so integrity checks run on-demand via sha256sum and stat rather than continuous background blocking. Blurry scans can lower OCR coverage, and save-text completion does not guarantee search-index readiness. External runtime dependencies: none."
    ),
]


def count_substantive_words():
    answers_only = " ".join(ans for _, ans in QUESTIONS_AND_ANSWERS)
    qa_combined = " ".join(f"{q} {ans}" for q, ans in QUESTIONS_AND_ANSWERS)
    ws_words = answers_only.split()
    alnum_tokens = re.findall(r"[A-Za-z0-9]+", answers_only)
    qa_ws_words = qa_combined.split()
    return {
        "substantive_whitespace_words": len(ws_words),
        "substantive_alnum_split_tokens": len(alnum_tokens),
        "questions_plus_answers_whitespace_words": len(qa_ws_words),
        "per_question_words": [(i + 1, len(ans.split())) for i, (_, ans) in enumerate(QUESTIONS_AND_ANSWERS)],
    }


def generate_pdf_v2():
    stats = count_substantive_words()
    print("=== WORD COUNT VERIFICATION ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    assert stats["substantive_whitespace_words"] <= 500, "Substantive word count exceeds 500!"
    assert stats["substantive_alnum_split_tokens"] <= 500, "Alnum token count exceeds 500!"

    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
    os.makedirs(dist_dir, exist_ok=True)
    pdf_path = os.path.join(dist_dir, "UGREEN_VaultSense_Proposal_v2.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=34,
        bottomMargin=34,
        title="VaultSense UGOS - UGREEN Hackathon 2026 Project Proposal",
        author="Khanhtnq",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleV2",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f766e"),
        spaceAfter=2,
    )
    sub_style = ParagraphStyle(
        "SubV2",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
        spaceAfter=4,
    )
    q_style = ParagraphStyle(
        "QuestionV2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=4,
        spaceAfter=1,
    )
    a_style = ParagraphStyle(
        "AnswerV2",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=2,
    )
    sec_style = ParagraphStyle(
        "SecV2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=6,
        spaceAfter=3,
    )
    cell_style = ParagraphStyle(
        "CellV2",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor("#1e293b"),
    )

    story = []

    # ==================== PAGE 1: 10 OFFICIAL QUESTIONS (<= 500 WORDS) ====================
    story.append(Paragraph("VaultSense UGOS (vaultsense-ugos) — Round 1 Project Proposal", title_style))
    story.append(Paragraph(
        f"UGREEN Hackathon 2026 on AI NAS | Track: Automate Your Workflow | Substantive Responses: {stats['substantive_whitespace_words']} / 500 English Words",
        sub_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#0d9488"), spaceBefore=1, spaceAfter=4))

    for q_text, a_text in QUESTIONS_AND_ANSWERS:
        story.append(Paragraph(q_text, q_style))
        story.append(Paragraph(a_text, a_style))

    story.append(PageBreak())

    # ==================== PAGE 2: EXCLUDED DECLARATIONS, SIGNATURES & LICENSES ====================
    story.append(Paragraph("Statutory Declarations, Signatures & Third-Party License Disclosures", title_style))
    story.append(Paragraph(
        "Excluded from the 500-word substantive limit per Official Rules (Round 1 Submission Requirements).",
        sub_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#0d9488"), spaceBefore=1, spaceAfter=6))

    story.append(Paragraph("1. Entrant / Team Consent Declaration & Electronic Signature", sec_style))
    story.append(Paragraph(
        "I, the undersigned Individual Entrant and sole Representative, hereby declare and confirm that: "
        "(a) I am the sole creator and owner of the submitted Project (<b>VaultSense UGOS / vaultsense-ugos</b>), and no uncredited outside party developed the Project or its submission materials; "
        "(b) the submitted Skill and core orchestration workflow were newly developed during the Hackathon Period without reusing previously published Skills or submission materials; and "
        "(c) I have read, understood, and consent to be bound by the UGREEN Hackathon 2026 on AI NAS Official Rules, Devpost Terms of Service, UGREEN SkillHub User Agreement, Privacy Policy, and Skill Content Safety and Publishing Guidelines.",
        a_style,
    ))
    story.append(Spacer(1, 4))

    sig_data = [
        [Paragraph("<b>Participation Structure</b>", cell_style), Paragraph("Individual Entrant (1 Member; Representative: Khanhtnq)", cell_style)],
        [Paragraph("<b>Member Name</b>", cell_style), Paragraph("Khanhtnq (GitHub / Devpost Handle: Khanhtnq)", cell_style)],
        [Paragraph("<b>Electronic Signature</b>", cell_style), Paragraph("<b>/s/ Khanhtnq</b>", cell_style)],
        [Paragraph("<b>Date Signed</b>", cell_style), Paragraph("November 15, 2026 (Pacific Time)", cell_style)],
    ]
    sig_table = Table(sig_data, colWidths=[145, 383])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Third-Party Components, Sources & Applicable Licenses", sec_style))
    story.append(Paragraph(
        "The Skill package (<code>ugreen_vaultsense_skill_v2.zip</code>) contains only original UTF-8 Markdown files (<code>SKILL.md</code> and <code>references/*.md</code>) licensed under the <b>MIT License</b> (Copyright (c) 2026 Khanhtnq). Authoring and validation used the following components:",
        a_style,
    ))
    story.append(Spacer(1, 3))

    lic_data = [
        [
            Paragraph("<b>Component / Tool</b>", cell_style),
            Paragraph("<b>Source</b>", cell_style),
            Paragraph("<b>Version</b>", cell_style),
            Paragraph("<b>License</b>", cell_style),
            Paragraph("<b>Scope of Use</b>", cell_style),
        ],
        [
            Paragraph("VaultSense UGOS Skill Package", cell_style),
            Paragraph("Original work by Khanhtnq", cell_style),
            Paragraph("2.0.0", cell_style),
            Paragraph("MIT License", cell_style),
            Paragraph("Submitted SKILL.md & references/*.md", cell_style),
        ],
        [
            Paragraph("UGOS Skill Creation Tool (uliya-skill-kit)", cell_style),
            Paragraph("America Ugreen Limited<br/>(ai.ugreen.com/pages/hackathon-starter-kit)", cell_style),
            Paragraph("0.7.7-en (Catalog 2.2.0)", cell_style),
            Paragraph("UGREEN Starter Kit & SkillHub Terms", cell_style),
            Paragraph("Capability catalog & check-skill.mjs static verification", cell_style),
        ],
        [
            Paragraph("Node.js Runtime", cell_style),
            Paragraph("OpenJS Foundation (nodejs.org)", cell_style),
            Paragraph("v20.x", cell_style),
            Paragraph("MIT License", cell_style),
            Paragraph("Local execution of check-skill.mjs (dev-time only)", cell_style),
        ],
        [
            Paragraph("Python & ReportLab", cell_style),
            Paragraph("PSF / ReportLab Inc. (pypi.org/project/reportlab)", cell_style),
            Paragraph("3.11 / 4.x", cell_style),
            Paragraph("PSF / BSD-3-Clause", cell_style),
            Paragraph("Generating this separate Proposal PDF only", cell_style),
        ],
    ]
    lic_table = Table(lic_data, colWidths=[108, 165, 65, 80, 110])
    lic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(lic_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. External Services, Data Flows & AI Tool Disclosures", sec_style))
    story.append(Paragraph(
        "• <b>External Services & Data Flows:</b> None. VaultSense UGOS calls zero external third-party APIs or servers; all file, OCR/VLM, and knowledge actions run within UGREEN AI NAS / Uliya registered experts on user-authorized folders.<br/>"
        "• <b>AI Tool Disclosure:</b> Claude / IDE AI coding assistant was used during development to cross-verify Uliya Capability Catalog 2.2.0 schemas, validate check-skill.mjs diagnostics, and polish grammar/table formatting.",
        a_style,
    ))

    doc.build(story)
    size_bytes = os.path.getsize(pdf_path)
    print(f"Generated {pdf_path} ({size_bytes} bytes, <= 1 MB limit: {size_bytes <= 1048576})")


if __name__ == "__main__":
    generate_pdf_v2()
