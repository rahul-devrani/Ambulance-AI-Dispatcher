import streamlit as st
import requests
import json
import heapq
import time
import multiprocessing
import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from env.engine import AmbulanceEngine


backend_app = FastAPI()
backend_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AmbulanceEngine()

@backend_app.post("/reset")
def reset(data: dict = Body(default={})):
    obs = engine.reset(data.get("p_loc"), data.get("p_sev"))
    return {"observation": obs, "reward": 0.0, "done": False}

@backend_app.post("/step")
def step(data: dict = Body(...)):
    next_node = data.get("next_node")
    obs, reward, done = engine.step(next_node)
    return {"observation": obs, "reward": float(reward), "done": bool(done), "info": {}}

def run_backend():
    uvicorn.run(backend_app, host="0.0.0.0", port=8000)


def run_frontend():
    st.set_page_config(page_title="Ambulance AI Dispatcher", layout="wide")

    st.markdown("""
        <style>
        .stButton>button { width: 100%; border-radius: 8px; background-color: #1a73e8; color: white; }
        .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #d1d5db; }
        </style>
    """, unsafe_allow_html=True)

    BASE_URL = "http://localhost:8000"


    with open("data/dehradun_map.json") as f:
        map_data = json.load(f)
    nodes, edges = map_data["nodes"], map_data["edges"]

    def get_optimal_path(start, end):
        queue = [(0, start, [])]
        seen = set()
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node not in seen:
                path = path + [node]
                if node == end: return path[1:]
                seen.add(node)
                for neighbor, weight in edges.get(node, {}).items():
                    heapq.heappush(queue, (cost + weight, neighbor, path))
        return []

    st.title("Ambulance Dispatcher AI")
    st.info("Dehradun Smart City Emergency Routing")


    with st.expander("Settings & Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            amb_start = st.selectbox("Ambulance Origin", list(nodes.keys()), index=0)
            pat_loc = st.selectbox("Patient Location", [n for n in nodes if nodes[n]['type']=='location'], index=31) # Bhaniyawala
        with col2:
            severity = st.radio("Patient Severity", ["Stable", "Critical"], horizontal=True)
            hospitals = [n for n in nodes if nodes[n]['type'] == 'hospital']
            target_hospital = "Max Hospital" if severity == "Critical" else "Doon Hospital"
            st.warning(f"Protocol: Triage to {target_hospital}")

    if st.button(" EXECUTE EMERGENCY ROUTING"):
        try:
            
            requests.post(f"{BASE_URL}/reset", json={"p_loc": pat_loc, "p_sev": severity})
            
           
            path_p = get_optimal_path(amb_start, pat_loc)
            path_h = get_optimal_path(pat_loc, target_hospital)
            
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Phase 1: Acquisition")
                p_bar = st.progress(0)
                for i, node in enumerate(path_p):
                    st.write(f" Arrived at: {node}")
                    requests.post(f"{BASE_URL}/step", json={"next_node": node})
                    p_bar.progress((i + 1) / len(path_p))
                    time.sleep(0.3)
            
            with c2:
                st.subheader(" Phase 2: Transfer")
                t_bar = st.progress(0)
                final_obs = None
                for i, node in enumerate(path_h):
                    st.write(f" Navigating: {node}")
                    res = requests.post(f"{BASE_URL}/step", json={"next_node": node}).json()
                    final_obs = res["observation"]
                    t_bar.progress((i + 1) / len(path_h))
                    time.sleep(0.3)

           
            st.markdown("---")
            st.subheader("Analytics")
            m1, m2, m3 = st.columns(3)
            health = final_obs['patient_health']
            m1.metric("Patient Vitals", f"{health}%")
            m2.metric("Total Steps", len(path_p) + len(path_h))
            m3.metric("Status", "SUCCESS" if health > 0 else "FAILED")

            if health > 0:
                st.success(f"Patient delivered to {target_hospital}")
            else:
                st.error("Patient vitals lost")

        except Exception as e:
            st.error(f"System Error: Ensure backend is running {e}")

    st.markdown("<br><hr><center>Developed by Rahul </center>", unsafe_allow_html=True)


if __name__ == "__main__":
  
    p = multiprocessing.Process(target=run_backend)
    p.start()
    run_frontend()
