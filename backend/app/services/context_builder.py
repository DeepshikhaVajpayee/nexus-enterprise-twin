from app.services.risk_service import calculate_project_risk
from app.state.enterprise_state import get_enterprise_state
from app.analytics.health_score import calculate_enterprise_health


def build_context():

    state = get_enterprise_state()
    health = calculate_enterprise_health()
    risk = calculate_project_risk("P1")

    return f"""
Enterprise Status

Health Score : {health['score']}
Status : {health['status']}

Operating Mode : {state['mode']}

Highest Risk Project :
{risk['project']}

Delay Probability :
{risk['delay_probability']}%

Root Causes:

{chr(10).join(risk['root_causes'])}
"""
