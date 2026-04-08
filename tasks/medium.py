def grade(state: dict) -> float:
    """
    MEDIUM TASK: Balance energy, focus, and stress for 1 full day.
    Grader returns a strict bounded float [0.0 - 1.0].
    """
    energy = float(state.get("energy", 0.0))
    focus = float(state.get("focus", 0.0))
    stress = float(state.get("stress", 100.0))
    
    e_pts = (energy / 100.0) * 0.33
    f_pts = (focus / 100.0) * 0.33
    s_pts = ((100.0 - stress) / 100.0) * 0.34
    
    score = e_pts + f_pts + s_pts
    return min(1.0, max(0.0, score))
