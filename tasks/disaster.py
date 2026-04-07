def setup_task(engine):
    # High pressure scenario
    engine.reset(p_sev="Critical")
    engine.patient_health = 60.0 # Start with low health
    return engine