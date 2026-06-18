from pydantic import BaseModel
from typing import Dict, Any


class EnterpriseEvent(BaseModel):
    event_type: str
    entity: str
    payload: Dict[str, Any] = {}
