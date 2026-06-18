class CompanyMemory:

    def __init__(self):
        self.events = []
        self.decisions = []
        self.risks = []

    def add_event(self, event):
        self.events.append(event)

    def add_decision(self, decision):
        self.decisions.append(decision)

    def add_risk(self, risk):
        self.risks.append(risk)

    def snapshot(self):
        return {
            "events": self.events,
            "decisions": self.decisions,
            "risks": self.risks
        }


memory = CompanyMemory()