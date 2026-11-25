from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from io import BytesIO


def score_suggestion(score):
    if score >= 85:
        return (
            "The student's academic performance is excellent. "
            "Maintaining strong study consistency, regular revision, "
            "and balanced lifestyle is recommended to continue success."
        )
    elif score >= 60:
        return (
            "The student is performing well but has room for improvement. "
            "Enhancing study techniques, focusing on weak subjects, "
            "and using available tutoring resources will help boost performance."
        )
    else:
        return (
            "The student needs support to improve performance. "
            "Structured study schedules, frequent teacher guidance, "
            "and stress reduction strategies are recommended."
        )


def generate_exam_report(student_name, data_dict, score, status):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    y = height - 50

    # ===== HEADER =====
    p.setFillColor(colors.HexColor("#0D2A78"))
    p.rect(0, height - 70, width, 70, fill=True, stroke=False)

    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(30, height - 45, "Exam Score Assessment Report")

    p.setFont("Helvetica", 10)
    p.drawRightString(
        width - 30, height - 45,
        f"{datetime.now().strftime('%Y-%m-%d   %H:%M:%S')}"
    )

    y -= 90

    # ===== SCORE BOX =====
    if score >= 85:
        box_color = colors.green
    elif score >= 60:
        box_color = colors.orange
    else:
        box_color = colors.red

    p.setFillColor(box_color)
    p.roundRect(30, y, 220, 50, 10, fill=True, stroke=False)

    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(45, y + 15, f"Exam Score: {score:.2f}")
    y -= 60

    # ===== STATUS =====
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, y, f"Status: {status}")
    y -= 30

    # ===== STUDENT DETAILS =====
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, y, "Student Information")
    y -= 25

    table_data = [["Feature", "Value"]]
    table_data.insert(1, ["Student Name", student_name])

    for k, v in data_dict.items():
        table_data.append([k.replace("_", " ").title(), str(v)])

    table = Table(table_data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D2A78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 30, y - table._height)
    y -= table._height + 40

    # ===== RECOMMENDATIONS =====
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, y, "Recommendations")
    y -= 25

    suggestions = score_suggestion(score)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11
    style.leading = 16

    formatted_suggestions = ""
    for sentence in suggestions.split(". "):
        formatted_suggestions += f"• {sentence.strip()}.<br/>"

    para = Paragraph(formatted_suggestions, style)

    frame = Frame(30, 50, width - 60, y - 30, showBoundary=0)
    frame.addFromList([para], p)

    # ===== FOOTER =====
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColor(colors.grey)
    p.drawString(
        30, 30,
        "This report is generated using AI — for academic support purposes only."
    )

    p.save()
    buffer.seek(0)
    return buffer
