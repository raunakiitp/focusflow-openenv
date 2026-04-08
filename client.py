from openenv import EnvClient
try:
    from .models import Action, Observation
except ImportError:
    from models import Action, Observation

class FocusFlowEnv(EnvClient):
    action_type = Action
    observation_type = Observation
