def setup_task(engine):
    engine.reset(p_sev="Stable")
    # Low health decay for midnight
    engine.health_decay = 0.5 
    return engine