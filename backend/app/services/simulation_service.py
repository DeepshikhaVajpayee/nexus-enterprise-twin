import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "enterprise_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def simulate_team_loss(engineers_lost: int):
    data = load_data()

    team = data["teams"][0]
    remaining_engineers = max(team["engineers"] - engineers_lost, 1)

    old_capacity = team["engineers"] * team["capacity_per_engineer"]
    new_capacity = remaining_engineers * team["capacity_per_engineer"]

    old_utilization = round((team["active_tasks"] / old_capacity) * 100)
    new_utilization = round((team["active_tasks"] / new_capacity) * 100)

    risk_increase = max(new_utilization - old_utilization, 0)

    affected_projects = [
        p["name"] for p in data["projects"] if p["team_id"] == team["id"]
    ]

    project_delay_days = engineers_lost * 7 + round(risk_increase / 5)

    return {
        "scenario": f'{team["name"]} loses {engineers_lost} engineers',
        "old_utilization": old_utilization,
        "new_utilization": new_utilization,
        "project_delay_days": project_delay_days,
        "risk_increase_percent": risk_increase,
        "affected_projects": affected_projects,
        "recommended_actions": [
            "Reduce parallel work",
            "Move engineers from lower-risk projects",
            "Escalate resource shortage",
            "Delay non-critical deliverables"
        ]
    }
