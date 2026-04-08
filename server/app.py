from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from env.engine import AmbulanceEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AmbulanceEngine()

@app.post("/reset")
def reset(data: dict = Body(default={})):
    obs = engine.reset(data.get("p_loc"), data.get("p_sev"))
    return {"observation": obs, "reward": 0.0, "done": False}

@app.post("/step")
def step(data: dict = Body(...)):
    next_node = data.get("next_node")
    obs, reward, done = engine.step(next_node)
    return {"observation": obs, "reward": float(reward), "done": bool(done), "info": {}}

@app.get("/state")
def state():
    return engine._obs("state")