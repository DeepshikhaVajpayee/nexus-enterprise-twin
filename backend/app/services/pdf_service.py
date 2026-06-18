from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.analytics.health_score import calculate_enterprise_health
from app.services.risk_service import calculate_project_risk
from app.reasoning.recommendation_engine import generate_recommendations
from app.services.timeline_service import get_timeline


def generate_ceo_report():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 60

    health = calculate_enterprise_health()
    risk = calculate_project_risk("P1")
    recommendations = generate_recommendations()
    timeline = get_timeline()

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "Nexus Enterprise Twin - CEO Report")

    y -= 40
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Enterprise Health: {health['score']} ({health['status']})")

    y -= 25
    pdf.drawString(50, y, f"Highest Risk Project: {risk.get('project')}")

    y -= 25
    pdf.drawString(50, y, f"Delay Probability: {risk.get('delay_probability')}%")

    y -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Root Causes")

    pdf.setFont("Helvetica", 11)
    for cause in risk.get("root_causes", []):
        y -= 20
        pdf.drawString(70, y, f"- {cause}")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Recommended Actions")

    pdf.setFont("Helvetica", 11)
    for rec in recommendations:
        y -= 20
        pdf.drawString(70, y, f"- [{rec['priority']}] {rec['action']}")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Recent Timeline")

    pdf.setFont("Helvetica", 11)
    for item in timeline[:5]:
        y -= 20
        pdf.drawString(70, y, f"- {item.get('time')} | {item.get('title')} | {item.get('description')}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
