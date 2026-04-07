def setup_task(engine):
    engine.reset(p_sev="Moderate")
    # Traffic simulation is naturally handled by traffic_sim.py
    return engine