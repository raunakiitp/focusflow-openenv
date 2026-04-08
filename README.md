---
title: Focusflow Env
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 👔 FocusFlow: Human Attention Optimization Environment

FocusFlow is a top-tier, highly realistic reinforcement learning environment built for the **Meta PyTorch OpenEnv Hackathon**. It completely bridges the gap between abstract AI scheduling and real-world human psychometric profiling.

## 📖 The Real-World Attention Crisis
In the modern workforce, AI agents cannot simply assign infinite tasks to humans. Humans suffer from dopamine burnout, focus fatigue, and stress collapses. FocusFlow simulates this absolute biological reality. 

If your AI agent forces a human to undergo `deep_work` while their `energy` is critically low (Burnout state), the human's psychological `stress` spikes and their long-term capacity crashes. This environment acts as a **dopamine and burnout regulation engine** for frontier models to practice genuine empathy-driven productivity.

## 🔬 Core Architecture (State & Action Space)

### The Deep Behavior State `(Observation)`
Tracked natively in `env/models.py`. The model evaluates strict psychological profiles:
- `energy`: Physical/Mental energy. Overworking near zero triggers massive burnout penalty modifiers.
- `focus`: Concentration tracking. Plummets if distractions hit.
- `stress`: Evaluated dynamically. Willpower intensive actions spike it.
- `temptation`, `distraction_level`, `deadline_pressure`, `progress`, `time_of_day`.
- *Bonus Vectors*: `consistency_streak` and `regret_matrix`.

### Human Workflow Engine `(Actions)`
- `deep_work`: High progress, massive energy drain.
- `light_work`: Safe incremental throughput.
- `take_break`: Critical restorative period.
- `scroll_social_media`: **The Dopamine Trap.** Immediately crushes `stress` and spikes short-term satisfaction, but fundamentally damages the hidden `regret_matrix` that penalizes future focus parameters heavily over subsequent steps.
- `block_distractions`, `switch_task`.

## 📈 The Composite Mathematical Reward Engine
We utilize a heavily integrated mathematical formula optimized for OpenEnv boundary verification `[0.0 - 1.0]`:
`raw_reward = (progress_gain * 0.5) + (focus * 0.3) - (stress * 0.4) - (distraction_time * 0.5) + (balance_score * 0.3)`

## 🏆 The Benchmark Tasks
We rigorously define 3 tasks with pure deterministic bounded `[0.0 - 1.0]` graders:
1. **Easy Task**: Avoid the `scroll` trap and natively reach 50% core progress.
2. **Medium Task**: Prove capability of stabilizing Energy, Focus, and Stress to survive a full day.
3. **Hard Task**: Multi-day high-deadline timeline handling compounding fatigue, burnout, and distraction levels.

## 🚀 Setup & Execution 

1. **Space Visualizer / Interface Check**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
   Navigate to the natively mounted Gradio/FastAPI server (passing `POST /reset` natively) to visualize the Psychometric Dashboard manually.

2. **Automated Baseline Inference**
   ```bash
   export API_BASE_URL="https://api.openai.com/v1"
   export MODEL_NAME="gpt-4o-mini"
   export HF_TOKEN="your-token"
   python inference.py
   ```
   The `inference.py` evaluator rigidly parses the required stdout formatting specification natively.
# trigger validation
