from app.memory.company_memory import memory


def get_enterprise_state():
    return {
        "health": 71,
        "active_projects": 4,
        "critical_risks": 3,
        "events": len(memory.events),
        "decisions": len(memory.decisions),
        "mode": "WATCHFUL"
    }