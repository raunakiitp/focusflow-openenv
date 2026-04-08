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
    energy: int = 100
    focus: int = 80
    stress: int = 20
    progress: int = 0
    step: int = 0
    done: bool = False
