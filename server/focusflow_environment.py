import random
from openenv import Environment
try:
    from ..models import Action, Observation, State
except ImportError:
    from models import Action, Observation, State

class FocusFlowEnvironment(Environment):
    def __init__(self):
        self.state = None

    async def reset(self, **kwargs) -> Observation:
        self.state = State(energy=100, focus=80, stress=20, progress=0, step=0, done=False)
        return Observation(**self.state.dict())

    async def step(self, action: Action) -> tuple:
        s = self.state
        s.step += 1

        if action.action == "deep_work":
            s.progress = min(100, s.progress + 15)
            s.energy = max(0, s.energy - 20)
            s.stress = min(100, s.stress + 5)
        elif action.action == "light_work":
            s.progress = min(100, s.progress + 7)
            s.energy = max(0, s.energy - 8)
        elif action.action == "take_break":
            s.energy = min(100, s.energy + 20)
            s.stress = max(0, s.stress - 10)
        elif action.action == "scroll_social_media":
            s.stress = max(0, s.stress - 5)
            s.focus = max(0, s.focus - 15)
        elif action.action == "block_distractions":
            s.focus = min(100, s.focus + 10)
        elif action.action == "switch_task":
            s.focus = max(0, s.focus - 5)
            s.progress = min(100, s.progress + 3)

        progress_gain = s.progress / 100
        raw_reward = (progress_gain * 0.5) + (s.focus/100 * 0.3) - (s.stress/100 * 0.4)
        reward = min(max(raw_reward, 0.0), 1.0)

        s.done = s.progress >= 100 or s.step >= 20
        obs = Observation(energy=s.energy, focus=s.focus, stress=s.stress, progress=s.progress, done=s.done)
        return obs, reward, s.done, {}

    async def state(self) -> State:
        return self.state
