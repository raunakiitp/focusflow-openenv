from openenv import EnvClient
from .models import Action, Observation

class FocusFlowEnv(EnvClient):
    action_type = Action
    observation_type = Observation
