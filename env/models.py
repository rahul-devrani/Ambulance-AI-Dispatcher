from pydantic import BaseModel
from typing import List, Dict

class Action(BaseModel):
    next_node: str

class Observation(BaseModel):
    current_node: str
    neighbors: List[str]
    patient_location: str
    target_hospital: str
    patient_health: float
    severity: str
    picked: bool
    steps: int
    message: str

class Reward(BaseModel):
    value: float
    breakdown: Dict[str, float]