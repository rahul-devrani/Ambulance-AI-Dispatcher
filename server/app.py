from fastapi import FastAPI, Body
from env.engine import AmbulanceEngine
from env.models import Action

app = FastAPI(title="Smart Ambulance AI")
engine = AmbulanceEngine()

@app.post("/reset")
async def reset(data: dict = Body(None)):
    p_loc = data.get("p_loc") if data else None
    p_sev = data.get("p_sev") if data else None
    return {"observation": engine.reset(p_loc, p_sev)}

@app.post("/step")
async def step(action: Action):
    obs, reward, done = engine.step(action.next_node)
    return {"observation": obs, "reward": reward, "done": done}

@app.get("/state")
async def state():
    return engine._obs("Current State")