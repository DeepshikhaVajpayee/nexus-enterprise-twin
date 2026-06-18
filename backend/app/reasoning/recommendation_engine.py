from app.analytics.health_score import calculate_enterprise_health
from app.services.risk_service import calculate_project_risk
from app.state.enterprise_state import get_enterprise_state
from app.services.context_builder import build_context
from app.services.llm_service import generate_llm_answer


def generate_recommendations():
    health = calculate_enterprise_health()
    risk = calculate_project_risk("P1")

    recommendations = []

    if health["score"] < 80:
        recommendations.append({
            "priority": "HIGH",
            "action": "Hold leadership review for current operational risks."
        })

    if risk.get("delay_probability", 0) >= 60:
        recommendations.append({
            "priority": "HIGH",
            "action": f"Focus on {risk.get('project', 'Project P1')} because delay probability is {risk.get('delay_probability')}%."
        })

    recommendations.append({
        "priority": "MEDIUM",
        "action": "Continue monitoring events, alerts, dependencies, and team workload."
    })

    return recommendations


def ask_ai_coo(question):
    health = calculate_enterprise_health()
    state = get_enterprise_state()
    risk = calculate_project_risk("P1")
    context = build_context()
    recommendations = generate_recommendations()

    try:
        answer = generate_llm_answer(question)
    except Exception as e:
        answer = (
            f"LLM unavailable, fallback used. Current health is {health['score']} "
            f"({health['status']}) and {risk.get('project', 'Project P1')} has "
            f"{risk.get('delay_probability')}% delay probability."
        )

    return {
        "question": question,
        "answer": answer,
        "context": context,
        "health": health,
        "enterprise_state": state,
        "risk": risk,
        "recommendations": recommendations
    }
