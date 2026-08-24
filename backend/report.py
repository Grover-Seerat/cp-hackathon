"""
report.py
Generates a court-style forensic PDF report for a single analyzed image.
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def create_pdf(case_id: str, result: dict, metadata: dict, sha256: str, timeline: list) -> str:
    """Builds the PDF and returns its filename (relative to REPORTS_DIR)."""
    filename = f"{case_id}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    doc = SimpleDocTemplate(
        filepath, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], textColor=colors.HexColor("#0b1f3a")
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], textColor=colors.HexColor("#0b1f3a"),
        spaceBefore=14, spaceAfter=6,
    )

    story = []
    story.append(Paragraph("TruthTrace AI — Digital Forensic Report", title_style))
    story.append(Paragraph("Chandigarh Police | AI Media Authenticity Investigation", styles["Normal"]))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#0b1f3a")))
    story.append(Spacer(1, 14))

    # Case summary
    story.append(Paragraph("Case Summary", section_style))
    case_table = Table([
        ["Case ID", case_id],
        ["Analyzed At (UTC)", metadata.get("analyzed_at_utc", "")],
        ["Original Filename", metadata.get("filename", "")],
        ["SHA-256 Hash", sha256],
    ], colWidths=[4.5 * cm, 11 * cm])
    case_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f3f9")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(case_table)

    # Detection result
    story.append(Paragraph("Authenticity Assessment", section_style))
    verdict = "AI-GENERATED / MANIPULATED" if result["label"].lower() in ("artificial", "fake", "ai") else "LIKELY AUTHENTIC"
    verdict_color = colors.HexColor("#b3261e") if "AI" in verdict or "MANIP" in verdict else colors.HexColor("#1e7d32")
    story.append(Paragraph(f'<font color="{verdict_color.hexval()}"><b>{verdict}</b></font>', styles["Normal"]))
    story.append(Spacer(1, 6))
    result_table = Table([
        ["Model Label", result["label"]],
        ["Confidence", f"{result['confidence']}%"],
    ], colWidths=[4.5 * cm, 11 * cm])
    result_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f3f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(result_table)

    # Image metadata
    story.append(Paragraph("Image Metadata", section_style))
    meta_rows = [
        ["Dimensions", f"{metadata.get('width')} x {metadata.get('height')}"],
        ["Format", metadata.get("format", "")],
        ["Color Mode", metadata.get("mode", "")],
        ["File Size", f"{metadata.get('size_bytes', 0):,} bytes"],
        ["EXIF Fields Found", str(len(metadata.get("exif", {})))],
    ]
    meta_table = Table(meta_rows, colWidths=[4.5 * cm, 11 * cm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f3f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)

    # Propagation timeline
    if timeline:
        story.append(Paragraph("Reconstructed Propagation Timeline", section_style))
        rows = [["Platform", "Timestamp"]] + [[t["platform"], t["time"]] for t in timeline]
        timeline_table = Table(rows, colWidths=[7.5 * cm, 8 * cm])
        timeline_table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b1f3a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(timeline_table)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This report was generated automatically by TruthTrace AI for investigative "
        "triage purposes. It is intended to assist, not replace, human forensic review.",
        styles["Italic"],
    ))

    doc.build(story)
    return filename
