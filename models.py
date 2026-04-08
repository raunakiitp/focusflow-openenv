from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    action: str

class Observation(BaseModel):
    energy: int
    focus: int
    stress: int
    progress: int
    done: bool = False

class State(BaseModel):
    energy: int
    focus: int
    stress: int
    progress: int
    step: int = 0
    done: bool = False
