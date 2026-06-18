import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "enterprise_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def calculate_project_risk(project_id: str = "P1"):
    data = load_data()

    project = next(p for p in data["projects"] if p["id"] == project_id)
    team = next(t for t in data["teams"] if t["id"] == project["team_id"])

    team_capacity = team["engineers"] * team["capacity_per_engineer"]
    utilization = round((team["active_tasks"] / team_capacity) * 100)

    risk_score = 0
    root_causes = []

    if utilization > 100:
        risk_score += 30
        root_causes.append(f'{team["name"]} utilization is {utilization}%')

    if project["blockers"] > 0:
        risk_score += project["blockers"] * 10
        root_causes.append(f'{project["blockers"]} unresolved blockers detected')

    if len(project["dependencies"]) > 0:
        risk_score += len(project["dependencies"]) * 15
        root_causes.append(f'{project["name"]} has {len(project["dependencies"])} active dependency')

    if project["progress"] < 50:
        risk_score += 20
        root_causes.append(f'{project["name"]} progress is only {project["progress"]}%')

    if project["deadline_days_left"] < 15:
        risk_score += 15
        root_causes.append("Deadline is approaching soon")

    delay_probability = min(risk_score, 95)

    if delay_probability >= 75:
        risk_level = "Critical"
    elif delay_probability >= 50:
        risk_level = "High"
    elif delay_probability >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "project": project["name"],
        "delay_probability": delay_probability,
        "confidence": 0.87,
        "risk_level": risk_level,
        "team_utilization": utilization,
        "root_causes": root_causes,
        "recommended_actions": [
            "Reduce active workload",
            "Resolve highest-priority blockers",
            "Reassign engineers to critical dependency",
            "Review project scope"
        ]
    }
