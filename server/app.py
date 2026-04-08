from openenv import create_app
try:
    from ..models import Action, Observation
except ImportError:
    from models import Action, Observation
try:
    from .focusflow_environment import FocusFlowEnvironment
except ImportError:
    from focusflow_environment import FocusFlowEnvironment

app = create_app(FocusFlowEnvironment, Action, Observation, env_name="focusflow_env")
