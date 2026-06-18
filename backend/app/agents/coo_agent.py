from app.services.risk_service import calculate_project_risk
from app.repositories.graph_repository import get_impact_chain


def generate_coo_brief(project_id: str = "P1"):
    risk = calculate_project_risk(project_id)
    impact = get_impact_chain(project_id)

    interventions = []

    if risk["delay_probability"] >= 75:
        interventions.append({
            "area": "Executive Escalation",
            "action": "Leadership should immediately review this project because delay probability is critical.",
            "expected_effect": "Reduces decision latency and accelerates blocker resolution."
        })

    if risk.get("team_utilization", 0) > 100:
        interventions.append({
            "area": "Resource Balancing",
            "action": "Move engineers from lower-risk initiatives to the overloaded team.",
            "expected_effect": "Reduces team overload and lowers delivery risk."
        })

    if len(risk.get("root_causes", [])) >= 3:
        interventions.append({
            "area": "Operational Focus",
            "action": "Run a focused risk review on blockers, dependencies, and scope.",
            "expected_effect": "Improves delivery confidence and clarifies ownership."
        })

    if not interventions:
        interventions.append({
            "area": "Monitoring",
            "action": "Continue monitoring project health.",
            "expected_effect": "Maintains visibility without unnecessary escalation."
        })

    return {
        "executive_summary": f'{risk["project"]} has a {risk["delay_probability"]}% delay probability. Main concern: {risk["root_causes"][0] if risk["root_causes"] else "no major blocker detected"}.',
        "leadership_focus": risk["root_causes"],
        "impact_chain": impact.get("impact_chain", []),
        "priority_interventions": interventions,
        "confidence": risk["confidence"]
    }
