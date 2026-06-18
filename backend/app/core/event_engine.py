from datetime import datetime
from app.services.risk_service import calculate_project_risk
from app.agents.coo_agent import generate_coo_brief

EVENT_LOG = []
ALERT_LOG = []


class EnterpriseEventEngine:
    def process_event(self, event: dict):
        event_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event.get("event_type"),
            "entity": event.get("entity"),
            "payload": event.get("payload", {})
        }

        EVENT_LOG.append(event_record)

        alert = self.generate_alert(event_record)
        ALERT_LOG.append(alert)

        return {
            "event_processed": event_record,
            "executive_alert": alert,
            "updated_intelligence": {
                "risk": calculate_project_risk("P1"),
                "coo_brief": generate_coo_brief("P1")
            }
        }

    def generate_alert(self, event):
        event_type = event["event_type"]

        if event_type == "DEPENDENCY_BLOCKED":
            return {
                "severity": "Critical",
                "title": "Dependency Blocked",
                "reason": f'{event["entity"]} has a blocked dependency affecting downstream delivery.',
                "recommended_action": "Escalate dependency owner and replan affected milestones."
            }

        if event_type == "EMPLOYEE_LEFT":
            return {
                "severity": "High",
                "title": "Team Capacity Reduced",
                "reason": "Team capacity dropped and active workload may exceed safe utilization.",
                "recommended_action": "Run resource simulation and rebalance critical work."
            }

        if event_type == "TICKET_CREATED":
            return {
                "severity": "Medium",
                "title": "Operational Signal Detected",
                "reason": "New ticket may indicate recurring operational friction.",
                "recommended_action": "Monitor ticket category and link it to affected project/team."
            }

        return {
            "severity": "Low",
            "title": "Enterprise Event Logged",
            "reason": "Event has been recorded for organizational memory.",
            "recommended_action": "No immediate intervention required."
        }

    def get_events(self):
        return EVENT_LOG

    def get_alerts(self):
        return ALERT_LOG


engine = EnterpriseEventEngine()
