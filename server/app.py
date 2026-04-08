import uvicorn
from openenv import create_app

try:
    from ..models import Action, Observation
except ImportError:
    from models import Action, Observation
try:
    from .environment import FocusFlowEnvironment
except ImportError:
    from environment import FocusFlowEnvironment

app = create_app(
    FocusFlowEnvironment,
    Action,
    Observation,
    env_name="focusflow_env"
)

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
