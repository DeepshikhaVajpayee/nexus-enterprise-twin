from pydantic import BaseModel
from typing import Optional


class Employee(BaseModel):
    id: str
    name: str
    role: str
    team: str
    utilization: float


class Team(BaseModel):
    id: str
    name: str
    utilization: float
    blockers: int


class Project(BaseModel):
    id: str
    name: str
    owner_team: str
    status: str
    progress: float
    deadline: str


class Risk(BaseModel):
    id: str
    name: str
    severity: str
    probability: float


class SimulationRequest(BaseModel):
    scenario: str
    entity_id: str
    impact_value: Optional[int] = 0
