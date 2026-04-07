def grade_task(obs, steps):
    # scoring between 0.0 and 1.0
    if obs["patient_health"] <= 0:
        return 0.0
        
    score = 0.0
    # 40% weightage: Survival Health
    score += (obs["patient_health"] / 100) * 0.4
    
    # 40% weightage: Destination matching (ICU for Critical)
    if obs["patient_severity"] == "Critical":
        icu_hospitals = ["Max Hospital", "Synergy Hospital", "AIIMS Rishikesh", "Velmed Hospital"]
        if obs["current_node"] in icu_hospitals:
            score += 0.4
        else:
            score += 0.1 # Penalty for wrong triage
    else:
        score += 0.4 # Stable patients can go anywhere
        
    # 20% weightage: Efficiency (Step count)
    if steps < 15:
        score += 0.2
    elif steps < 30:
        score += 0.1
        
    return round(min(score, 1.0), 2)