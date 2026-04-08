import os
import json
import asyncio
from typing import List
from openai import OpenAI

from server.focusflow_environment import FocusFlowEnvironment
from models import Action
from tasks import easy, medium, hard

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    print(f"[STEP] step={step} action={action!r} reward={reward:+.2f} done={done} error={error}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    print(f"[END] success={success} steps={steps} score={score:.2f} rewards={rewards}", flush=True)

def get_action_from_llm(client, model_name, state):
    prompt = f"""
    You are a profound RL AI operating a strict 'Human Psychometric' model.
    You must intelligently push tasks utilizing specific workflows.
    
    State:
    - Energy: {state.energy}
    - Focus: {state.focus}
    - Stress: {state.stress}
    - Progress: {state.progress}
    
    Valid action_types:
    "deep_work", "light_work", "take_break", "scroll_social_media", "block_distractions", "switch_task"
    
    Strategy:
    If Energy is low, take_break. Otherwise focus on deep_work and light_work.
    
    Output strictly valid JSON:
    {{"action": "..."}}
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You output strict JSON exclusively."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return Action(action=data.get("action", "take_break"))
    except Exception:
        return Action(action="take_break")

async def run_evaluation(client, model_name, difficulty, grader_func):
    env = FocusFlowEnvironment()
    state = await env.reset()
    done = False
    
    log_start(task=difficulty, env="FocusFlow Meta", model=model_name)
    
    rewards = []
    steps_taken = 0
    
    while not done:
        steps_taken += 1
        action = get_action_from_llm(client, model_name, state)
             
        action_dict = json.dumps(action.model_dump(exclude_none=True))
        state, reward, done, _ = await env.step(action)
        
        rewards.append(reward)
        log_step(step=steps_taken, action=action_dict, reward=reward, done=done, error=None)
        
    score = grader_func(state.model_dump())
    score = min(max(score, 0.0), 1.0)
    success = score >= 0.5 
    
    log_end(success=success, steps=steps_taken, score=score, rewards=rewards)
    return score

async def main():
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    # Check if necessary env vars are missing during local check
    if HF_TOKEN is None:
        print("[WARNING] HF_TOKEN is missing. Defaulting to local dry runs.")
        HF_TOKEN = "dummy-token"
        
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    
    await run_evaluation(client, MODEL_NAME, "easy", easy.grade)
    await run_evaluation(client, MODEL_NAME, "medium", medium.grade)
    await run_evaluation(client, MODEL_NAME, "hard", hard.grade)

if __name__ == "__main__":
    asyncio.run(main())
