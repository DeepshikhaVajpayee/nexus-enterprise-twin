from fastapi import APIRouter
from pydantic import BaseModel

from app.services.risk_service import calculate_project_risk
from app.services.simulation_service import simulate_team_loss
from app.agents.coo_agent import generate_coo_brief
from app.services.impact_service import propagate_project_delay
from app.core.event_engine import engine
from app.schemas.events import EnterpriseEvent
from app.services.briefing_service import generate_executive_briefing

from app.state.enterprise_state import get_enterprise_state
from app.analytics.health_score import calculate_enterprise_health
from app.reasoning.recommendation_engine import generate_recommendations, ask_ai_coo

from app.services.timeline_service import add_timeline, get_timeline
from app.services.executive_alert_service import create_alert_from_event, get_autonomous_alerts
from app.services.auth_service import authenticate_user


router = APIRouter(prefix="/api", tags=["Enterprise Intelligence"])


class COOQuestion(BaseModel):
    question: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/graph/live")
def graph_live():
    return [
        {"source": "Project Alpha", "relation": "DEPENDS_ON", "target": "Project Beta"},
        {"source": "Project Beta", "relation": "OWNED_BY", "target": "Team X"},
        {"source": "Team X", "relation": "HAS_RISK", "target": "Resource Overload"},
    ]


@router.get("/coo/brief")
def coo_brief():
    return generate_coo_brief("P1")


@router.get("/risk/{project_id}")
def project_risk(project_id: str):
    return calculate_project_risk(project_id)


@router.get("/simulate/team-loss/{engineers_lost}")
def simulate(engineers_lost: int):
    return simulate_team_loss(engineers_lost)


@router.get("/impact/project-slip/{project_name}/{delay_days}")
def project_slip_impact(project_name: str, delay_days: int):
    clean_name = project_name.replace("-", " ")
    return propagate_project_delay(clean_name, delay_days)


@router.post("/events")
def ingest_event(event: EnterpriseEvent):
    result = engine.process_event(event.dict())

    create_alert_from_event(event.event_type, event.entity)

    add_timeline(
        event.event_type,
        f"{event.entity} triggered an enterprise event.",
        {
            "health_delta": "-4",
            "risk_delta": "+3",
            "alert_generated": True,
        },
    )

    return result


@router.get("/events")
def get_events():
    return engine.get_events()


@router.get("/alerts")
def get_alerts():
    return engine.get_alerts()


@router.get("/autonomous-alerts")
def autonomous_alerts():
    return get_autonomous_alerts()


@router.get("/timeline")
def timeline():
    return get_timeline()


@router.get("/executive/briefing")
def executive_briefing():
    return generate_executive_briefing()


@router.get("/enterprise/state")
def enterprise_state():
    return get_enterprise_state()


@router.get("/enterprise/health")
def enterprise_health():
    return calculate_enterprise_health()


@router.get("/enterprise/recommendations")
def enterprise_recommendations():
    return generate_recommendations()


@router.post("/coo/ask")
def coo_ask(data: COOQuestion):
    return ask_ai_coo(data.question)



class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/login")
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    return {
        "success": True,
        "message": "Login successful",
        **user
    }

from fastapi.responses import StreamingResponse
from app.services.pdf_service import generate_ceo_report

@router.get("/reports/ceo")
def ceo_report():
    pdf = generate_ceo_report()
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ceo_report.pdf"}
    )
