from pydantic import BaseModel

class Observation(BaseModel):
    energy: int
    focus: int
    stress: int
    progress: int

class Action(BaseModel):
    action: str

class Reward(BaseModel):
    reward: float
