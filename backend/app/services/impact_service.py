def propagate_project_delay(project_name: str, delay_days: int):
    dependency_map = {
        "Project Beta": [
            {
                "affected_entity": "Project Alpha",
                "impact_type": "Delivery Delay",
                "estimated_delay_days": round(delay_days * 0.7),
                "severity": "High"
            },
            {
                "affected_entity": "Customer Onboarding",
                "impact_type": "Business Outcome Delay",
                "estimated_delay_days": round(delay_days * 0.5),
                "severity": "Medium"
            },
            {
                "affected_entity": "Team X",
                "impact_type": "Workload Increase",
                "estimated_delay_days": 0,
                "severity": "High"
            }
        ]
    }

    impacts = dependency_map.get(project_name, [])

    risk_score = min(95, delay_days * 4 + len(impacts) * 12)

    return {
        "scenario": f"{project_name} slips by {delay_days} days",
        "risk_score": risk_score,
        "affected_count": len(impacts),
        "impact_chain": impacts,
        "recommended_actions": [
            "Escalate dependency owner",
            "Replan downstream milestones",
            "Notify affected stakeholders",
            "Move support to critical path"
        ]
    }
