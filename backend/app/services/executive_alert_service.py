alerts = []


def add_alert(title, severity, reason, recommended_action):
    alerts.append({
        "title": title,
        "severity": severity,
        "reason": reason,
        "recommended_action": recommended_action
    })


def get_autonomous_alerts():
    return alerts[::-1]


def create_alert_from_event(event_type, entity):
    if event_type == "DEPENDENCY_BLOCKED":
        add_alert(
            "Dependency Blocked",
            "HIGH",
            f"{entity} has a blocked dependency affecting delivery.",
            "Escalate blocker and assign senior owner immediately."
        )

    elif event_type == "EMPLOYEE_LEFT":
        add_alert(
            "Resource Loss Detected",
            "HIGH",
            f"{entity} lost a critical team member.",
            "Rebalance workload and assign backup ownership."
        )

    elif event_type == "TICKET_CREATED":
        add_alert(
            "New Operational Signal",
            "MEDIUM",
            f"New ticket created for {entity}.",
            "Review ticket priority and impact on delivery."
        )
