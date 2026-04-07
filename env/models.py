from pydantic import BaseModel
from typing import List

class Action(BaseModel):
    next_node: str

class Observation(BaseModel):
    current_node: str
    neighbors: List[str]
    patient_location: str
    target_hospital: str
    patient_health: float
    patient_severity: str
    phase: str
    message: str