from fastapi import FastAPI
import gradio as gr
import uvicorn
from typing import Any, Dict

from focusflow_env.server.environment import FocusEnv
from focusflow_env.models import Action

app = FastAPI()
env = FocusEnv(difficulty="hard")
_state = env.reset()

@app.post("/reset")
def api_reset(payload: Dict[Any, Any] = None):
    global _state
    _state = env.reset()
    return _state.dict()

@app.get("/state")
def api_state():
    return _state.dict()

@app.post("/step")
def api_step(action: Action):
    global _state
    state, reward, done, info = env.step(action)
    _state = state
    return {
        "observation": state.dict(),
        "reward": {"value": reward, "reason": info.get("reason", "")},
        "done": done,
        "info": info
    }

def gradio_step(action_choice):
    global _state, env
    
    if action_choice == "Reset":
        _state = env.reset()
        return _state.energy, _state.focus, _state.stress, env.temptation, env.time_of_day, env.deadline_pressure, _state.progress, env.distraction_level, env.status_log, "Environment restarted."
        
    if getattr(_state, "progress", 0) >= 100 or getattr(env, "day_count", 0) > 3:
         return _state.energy, _state.focus, _state.stress, env.temptation, env.time_of_day, env.deadline_pressure, _state.progress, env.distraction_level, env.status_log, "Submission Complete."

    a_type = action_choice
    act = Action(action=a_type)
    
    _state, reward, done, info = env.step(act)
    status = f"Action: {action_choice}\nReward Signal: {reward:.2f}\nLog: {info.get('reason', '')}"
    if done:
        status += "\n\n🏁 SHIFT COMPLETE."
        
    return _state.energy, _state.focus, _state.stress, env.temptation, env.time_of_day, env.deadline_pressure, _state.progress, env.distraction_level, env.status_log, status

with gr.Blocks(title="FocusFlow Meta Submit", theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 👔 FocusFlow: Meta PyTorch OpenEnv by Comet")
    gr.Markdown("Real-world human attention optimization environment. Test the agent actions natively below.")
    
    with gr.Row():
         with gr.Column():
             gr.Markdown("### Psychological State Matrix")
             energy_bar = gr.Number(label="⚡ Energy", value=_state.energy, interactive=False)
             focus_bar = gr.Number(label="🎯 Focus", value=_state.focus, interactive=False)
             stress_bar = gr.Number(label="😫 Stress", value=_state.stress, interactive=False)
             temp_bar = gr.Number(label="📱 Temptation", value=env.temptation, interactive=False)
                 
         with gr.Column():
             gr.Markdown("### Environmental Pressures")
             time_bar = gr.Textbox(label="Time of Day", value=env.time_of_day, interactive=False)
             dead_bar = gr.Number(label="Deadline Pressure", value=env.deadline_pressure, interactive=False)
             dist_bar = gr.Number(label="Distraction Level", value=env.distraction_level, interactive=False)
             prog_bar = gr.Number(label="Total Progress", value=_state.progress, interactive=False)
                 
    status_log = gr.Textbox(label="Last Internal Event Target", value=env.status_log, interactive=False)
    status_out = gr.Textbox(label="Console Stream", lines=2, value="Ready.")
    
    with gr.Row():
         dw_btn = gr.Button("deep_work", variant="primary")
         lw_btn = gr.Button("light_work")
         tb_btn = gr.Button("take_break")
    with gr.Row():
         ssm_btn = gr.Button("scroll_social_media", variant="stop")
         bd_btn = gr.Button("block_distractions", variant="secondary")
         st_btn = gr.Button("switch_task")
         
    rst_btn = gr.Button("Reset Simulation")
             
    outputs = [energy_bar, focus_bar, stress_bar, temp_bar, time_bar, dead_bar, prog_bar, dist_bar, status_log, status_out]
    
    dw_btn.click(fn=lambda: gradio_step("deep_work"), outputs=outputs)
    lw_btn.click(fn=lambda: gradio_step("light_work"), outputs=outputs)
    tb_btn.click(fn=lambda: gradio_step("take_break"), outputs=outputs)
    ssm_btn.click(fn=lambda: gradio_step("scroll_social_media"), outputs=outputs)
    bd_btn.click(fn=lambda: gradio_step("block_distractions"), outputs=outputs)
    st_btn.click(fn=lambda: gradio_step("switch_task"), outputs=outputs)
    rst_btn.click(fn=lambda: gradio_step("Reset"), outputs=outputs)

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run("focusflow_env.server.app:app", host="0.0.0.0", port=7860)
