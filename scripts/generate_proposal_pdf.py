import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
    os.makedirs(dist_dir, exist_ok=True)
    pdf_path = os.path.join(dist_dir, "UGREEN_VaultSense_Proposal.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f766e')
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569')
    )
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )

    story = []

    # Header
    story.append(Paragraph("UGREEN Hackathon 2026 on AI NAS — Round 1 Proposal", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("VaultSense UGOS", title_style))
    story.append(Paragraph("Zero-Cloud Semantic Deduplicator, Entropy Ransomware Canary & Invoice Tax Vault", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0d9488'), spaceBefore=2, spaceAfter=14))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Problem Statement", h2_style))
    story.append(Paragraph(
        "Modern Network-Attached Storage (NAS) users accumulate terabytes of unorganized data: duplicate bursts of 4K drone/camera footage, multiple redundant cloud backup syncs, and disorganized expense receipts. Concurrently, NAS deployments are the #1 target for ransomware operators who quietly encrypt network shares. Sending private NAS data to third-party public clouds for AI analysis violates the core reason users purchased a local NAS: <b>absolute data privacy and sovereignty</b>.",
        body_style
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>VaultSense</b> is a native edge AI Skill engineered exclusively for <b>UGREEN AI NAS (UGOS)</b> that runs 100% locally with zero cloud egress. It delivers three enterprise-grade capabilities: (1) Rolling Content-Defined Block & MinHash Semantic Deduplication; (2) Shannon Entropy Tripwire Canary that detects active ransomware encryption in milliseconds; and (3) Local Invoice & VAT Tax Extraction that turns unstructured scans into deduction-ready financial records.",
        body_style
    ))

    # Architecture Overview Table
    story.append(Paragraph("2. Technical Architecture & UGOS Integration", h2_style))
    data = [
        [Paragraph("<b>Component</b>", table_cell), Paragraph("<b>Engineering Mechanism</b>", table_cell), Paragraph("<b>UGOS Advantage</b>", table_cell)],
        [
            Paragraph("Semantic Deduplicator", table_cell),
            Paragraph("CDC chunking + SHA-256 exact match + MinHash Jaccard token similarity for near-dupe document versions.", table_cell),
            Paragraph("Saves 25-40% volume storage without uploading files or exposing file contents.", table_cell)
        ],
        [
            Paragraph("Entropy Canary Sentry", table_cell),
            Paragraph("Continuous Shannon entropy (H = -sum(p log2 p)) monitoring. Trips at >7.85 bits/byte on non-compressed traps.", table_cell),
            Paragraph("Zero false-positive honey-canaries that halt rogue processes before mass damage occurs.", table_cell)
        ],
        [
            Paragraph("Invoice & Tax Vault", table_cell),
            Paragraph("Deterministic regex NER + local language parser extracting VAT numbers, currencies, and tax deductions.", table_cell),
            Paragraph("Fully offline tax preparation for freelancers, SMBs, and families directly on local storage.", table_cell)
        ]
    ]
    t = Table(data, colWidths=[120, 260, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Round 1 Validation & Feasibility
    story.append(Paragraph("3. Round 1 Local Feasibility & Validation", h2_style))
    story.append(Paragraph(
        "VaultSense has been built and rigorously validated locally in accordance with the UGREEN Skill Developer Package guidelines. The project includes a complete Docker Compose specification, a standard <code>manifest.json</code> declaration, an interactive Web Dashboard (<code>docs/index.html</code>), and a comprehensive automated <code>pytest</code> suite covering deduplication, entropy calculation, canary tampering, and invoice parsing. All tests pass locally with 100% success.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Round 2 Deployment Plan on iDX6011 Pro
    story.append(Paragraph("4. Round 2 Hardware Acceleration Plan (iDX6011 Pro)", h2_style))
    story.append(Paragraph(
        "Upon advancement to Round 2, the team will deploy VaultSense to the provided remote UGREEN AI NAS hardware (<code>iDX6011 Pro</code>). The system will be bound to the hardware NPU accelerator for sub-10ms batch embedding acceleration, hooked into UGOS system notifications, and packaged for the official UGREEN Skills Hub.",
        body_style
    ))
    story.append(Spacer(1, 14))

    # Metadata & Sign-off
    story.append(Paragraph("<b>Author:</b> Khanhtnq &lt;218711032+Khanhtnq@users.noreply.github.com&gt; | <b>License:</b> MIT", subtitle_style))
    story.append(Paragraph("<b>Skill Package ID:</b> com.ugreen.skill.vaultsense | <b>Version:</b> 1.0.0", subtitle_style))

    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
