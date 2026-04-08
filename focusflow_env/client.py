import os
import requests
from typing import Dict, Any, Tuple

try:
    from openenv import EnvClient
except ImportError:
    class EnvClient:
        pass

from .models import Action, Observation

class FocusEnvClient(EnvClient):
    def __init__(self, base_url: str = None):
        # Allow connecting natively to the local FastAPI or a deployed HF space
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:7860")

    def reset(self) -> Observation:
        response = requests.post(f"{self.base_url}/reset", json={})
        response.raise_for_status()
        return Observation(**response.json())

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        response = requests.post(f"{self.base_url}/step", json=action.dict())
        response.raise_for_status()
        data = response.json()
        
        obs = Observation(**data["observation"])
        reward = float(data["reward"]["value"])
        done = bool(data["done"])
        info = data.get("info", {})
        
        return obs, reward, done, info
