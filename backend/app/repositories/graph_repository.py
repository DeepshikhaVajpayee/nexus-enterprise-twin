ENTERPRISE_GRAPH = {
    "projects": [
        {
            "id": "P1",
            "name": "Project Alpha",
            "status": "At Risk",
            "progress": 42,
            "owner_team": "Team X",
            "deadline": "2026-08-30"
        },
        {
            "id": "P2",
            "name": "Project Beta",
            "status": "Delayed",
            "progress": 55,
            "owner_team": "Team X",
            "deadline": "2026-07-20"
        }
    ],
    "teams": [
        {
            "id": "T1",
            "name": "Team X",
            "utilization": 118,
            "blockers": 3
        }
    ],
    "relationships": [
        {
            "source": "Project Alpha",
            "relation": "DEPENDS_ON",
            "target": "Project Beta"
        },
        {
            "source": "Project Beta",
            "relation": "OWNED_BY",
            "target": "Team X"
        },
        {
            "source": "Team X",
            "relation": "HAS_RISK",
            "target": "Resource Overload"
        }
    ]
}


def get_enterprise_graph():
    return ENTERPRISE_GRAPH


def get_impact_chain(project_id: str):
    if project_id == "P1":
        return {
            "project": "Project Alpha",
            "impact_chain": [
                "Project Alpha depends on Project Beta",
                "Project Beta is owned by Team X",
                "Team X is overloaded at 118%",
                "Team X has 3 unresolved blockers",
                "Delay probability increases to 82%"
            ]
        }

    return {
        "project_id": project_id,
        "impact_chain": []
    }
