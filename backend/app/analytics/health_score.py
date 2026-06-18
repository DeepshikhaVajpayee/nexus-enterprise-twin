from app.state.enterprise_state import get_enterprise_state


def calculate_enterprise_health():
    state = get_enterprise_state()

    score = 100
    score -= state["critical_risks"] * 10
    score -= state["events"] * 2

    if score < 0:
        score = 0

    return {
        "score": score,
        "status": (
            "Healthy"
            if score > 80
            else "Watchful"
            if score > 50
            else "Critical"
        )
    }