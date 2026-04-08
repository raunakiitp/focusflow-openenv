def grade(state: dict) -> float:
    """
    EASY TASK: Avoid distractions and reach 50% progress.
    Grader returns a strict bounded float [0.0 - 1.0].
    """
    progress = min(50.0, float(state.get("progress", 0.0)))
    distraction = float(state.get("distraction_level", 10.0))
    
    score = (progress / 50.0) * 0.7
    if distraction < 30.0:
        score += 0.3
        
    return min(1.0, max(0.0, score))
