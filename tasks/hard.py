def grade(state: dict) -> float:
    """
    HARD TASK: Optimize productivity over multiple days with deadlines, fatigue, and distractions.
    Grader returns a strict bounded float [0.0 - 1.0].
    """
    progress = min(100.0, float(state.get("progress", 0.0)))
    deadline_pressure = float(state.get("deadline_pressure", 100.0))
    regret = float(state.get("regret_matrix", 10.0))
    
    score = (progress / 100.0) * 0.6
    
    if deadline_pressure < 80.0:
        score += 0.2
    if regret < 2.0:
        score += 0.2
        
    return min(1.0, max(0.0, score))
