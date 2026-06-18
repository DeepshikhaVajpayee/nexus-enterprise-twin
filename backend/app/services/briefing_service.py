from app.services.risk_service import calculate_project_risk
from app.agents.coo_agent import generate_coo_brief
from app.core.event_engine import engine


def generate_executive_briefing():
    risk = calculate_project_risk("P1")
    coo = generate_coo_brief("P1")
    events = engine.get_events()
    alerts = engine.get_alerts()

    return {
        "title": "Executive Intelligence Briefing",
        "summary": f'{risk["project"]} is currently at {risk["delay_probability"]}% delivery risk with {len(alerts)} executive alerts active.',
        "enterprise_health": {
            "status": "At Risk" if risk["delay_probability"] >= 70 else "Stable",
            "delay_probability": risk["delay_probability"],
            "confidence": risk["confidence"]
        },
        "top_risks": risk["root_causes"],
        "active_alerts": alerts,
        "recent_events": events[-5:],
        "recommended_actions": [
            item["action"] for item in coo.get("priority_interventions", [])
        ]
    }
