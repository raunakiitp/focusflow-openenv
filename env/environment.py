import random
from typing import Tuple, Dict, Any
from .models import Observation, Action

class FocusEnv:
    def __init__(self, difficulty: str = "hard"):
        self.difficulty = difficulty
        self.step_count = 0
        
        self.distraction_level = 10.0
        self.temptation = 80.0
        self.consistency_streak = 0
        self.regret_matrix = 0.0
        self.day_count = 1
        self.time_of_day = "morning"
        self.deadline_pressure = 10.0
        self.status_log = "Environment reset."
        
        self.reset()

    def reset(self) -> Observation:
        self.state = {
            "energy": 100,
            "focus": 50,
            "stress": 20,
            "progress": 0
        }
        
        initial_deadline = 10.0
        if self.difficulty == "hard":
            initial_deadline = 60.0
        elif self.difficulty == "easy":
            initial_deadline = 0.0
            
        self.distraction_level = 10.0
        self.temptation = 80.0
        self.consistency_streak = 0
        self.regret_matrix = 0.0
        self.day_count = 1
        self.time_of_day = "morning"
        self.deadline_pressure = initial_deadline
        self.status_log = "Environment reset."
        
        self.step_count = 0
        return Observation(**self.state)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.step_count += 1
        event_message = ""
        
        energy = float(self.state["energy"])
        focus = float(self.state["focus"])
        stress = float(self.state["stress"])
        progress = float(self.state["progress"])
        
        # 1. Human Behavior: Random Events
        event_roll = random.random()
        if event_roll < 0.1:
            self.distraction_level += 30
            self.temptation += 20
            event_message = "[Notification Ping] "
        elif event_roll < 0.2:
            energy -= 20
            focus -= 15
            event_message = "[Sudden Fatigue] "
        elif event_roll < 0.25:
            stress += 30
            event_message = "[Mood Swing] "

        progress_gain = 0.0
        distraction_time = 0.0
        
        # Human Behavior: Burnout system & Regret
        burnout_penalty = 0.0
        if energy < 20:
             burnout_penalty = 1.0 
             stress += 10
        if self.regret_matrix > 0:
             focus -= self.regret_matrix * 5
             self.regret_matrix = max(0, self.regret_matrix - 1)

        # Action Execution Space
        act = action.action
        if act == "deep_work":
            if focus > 30 and energy > 20:
                progress_gain = 15.0 - (self.distraction_level * 0.1) 
                energy -= 25
                stress += 15
                self.consistency_streak += 1
            else:
                stress += 25 
                self.consistency_streak = 0
        elif act == "light_work":
            progress_gain = 5.0
            energy -= 10
            stress += 5
            self.consistency_streak += 1
        elif act == "take_break":
            energy = min(100, energy + 30)
            stress = max(0, stress - 25)
            focus = min(100, focus + 15)
            self.consistency_streak = 0
        elif act == "scroll_social_media":
            distraction_time = 1.0
            stress = max(0, stress - 30) # immediate drop
            energy = max(0, energy - 5)
            self.temptation = max(0, self.temptation - 50)
            self.regret_matrix += 3 # Top 5% bonus: Long term pain
            self.consistency_streak = 0
        elif act == "block_distractions":
            self.distraction_level = max(0, self.distraction_level - 40)
            self.temptation = max(0, self.temptation - 20)
            stress += 10 
            self.consistency_streak = 0
        elif act == "switch_task":
            focus -= 20
            stress = max(0, stress - 10)
            self.consistency_streak += 1

        balance_score = ((energy + focus + (100 - stress)) / 300.0) * 10.0
        progress_gain = max(0.0, progress_gain * (1.0 - burnout_penalty * 0.5))
        progress = min(100.0, progress + progress_gain)
        
        # Dynamics: Shifts & Deadlines
        idx = (self.step_count // 5) % 3
        self.time_of_day = ["morning", "afternoon", "night"][idx]
        
        if self.step_count > 0 and self.step_count % 15 == 0:
            self.day_count += 1
            energy = min(100, energy + 50) 
            stress = max(0, stress - 40)
            self.deadline_pressure = min(100, self.deadline_pressure + 20) 
            
        # 2. Strict Mathematical Composite Reward Target
        raw_reward = ((progress_gain * 0.4) 
                      + ((focus/10.0) * 0.3) 
                      - ((stress/10.0) * 0.3) 
                      - (distraction_time * 0.5) 
                      + (balance_score * 0.2))
                      
        raw_reward += (self.consistency_streak * 0.1) # bonus
        
        scaled_reward = (raw_reward + 5.0) / 10.0
        step_reward = min(1.0, max(0.0, scaled_reward))
        
        # Clamp observation targets natively to int
        self.state["energy"] = int(min(100.0, max(0.0, energy)))
        self.state["focus"] = int(min(100.0, max(0.0, focus)))
        self.state["stress"] = int(min(100.0, max(0.0, stress)))
        self.state["progress"] = int(min(100.0, max(0.0, progress)))
        
        # Episode ends map
        done = False
        if self.difficulty == "easy" and progress >= 50.0:
            done = True
        elif self.difficulty == "medium" and self.day_count > 1:
            done = True
        elif self.difficulty == "hard" and self.day_count > 7:
            done = True
            
        if progress >= 100.0:
             done = True

        reason = event_message + f"Executed '{act}'."
        self.status_log = reason
        
        obs = Observation(
            energy=self.state["energy"],
            focus=self.state["focus"],
            stress=self.state["stress"],
            progress=self.state["progress"]
        )
        return obs, float(step_reward), done, {"reason": reason}
