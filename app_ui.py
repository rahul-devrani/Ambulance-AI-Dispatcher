import streamlit as st
import requests
import json
import heapq
import time
from typing import List

# UI Configuration
st.set_page_config(
    page_title="Ambulance AI Dispatcher",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS Styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5rem;
        background-color: #1a73e8;
        color: white;
        font-weight: bold;
    }
    .status-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        margin-bottom: 1rem;
    }
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a202c;
        color: #ffffff;
        text-align: center;
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

BASE_URL = "http://localhost:7860"

# Load city graph data
@st.cache_data
def load_map_data():
    with open("data/dehradun_map.json") as f:
        data = json.load(f)
    return data["nodes"], data["edges"]

nodes, edges = load_map_data()

# Shortest path calculation logic
def get_optimal_path(start: str, end: str) -> List[str]:
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

# Application Header
st.title("Ambulance Dispatcher AI")
st.markdown("---")

# Input Section
with st.container():
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        amb_start = st.selectbox("Ambulance Origin", list(nodes.keys()), index=12)
        pat_loc = st.selectbox("Patient Location", [n for n in nodes if nodes[n]['type']=='location'], index=0)
        severity = st.radio("Patient Condition", ["Stable", "Critical"], horizontal=True)
    
    with col2:
        hospitals = [n for n in nodes if nodes[n]['type'] == 'hospital']
        if severity == "Stable":
            target_hospital = st.selectbox("Target Facility (Manual Select)", hospitals)
        else:
            # Automated triage for critical patients
            icu_hospitals = [h for h in hospitals if nodes[h].get("has_icu")]
            target_hospital = icu_hospitals[0] if icu_hospitals else hospitals[0]
            st.warning(f"Protocol: Critical triage to {target_hospital}")

    run_btn = st.button("EXECUTE")
    st.markdown('</div>', unsafe_allow_html=True)

# Execution Flow
if run_btn:
    try:
        # Synchronize with environment server
        res = requests.post(f"{BASE_URL}/reset", json={
            "p_loc": pat_loc, 
            "p_sev": severity,
            "target_hosp": target_hospital
        }).json()
        
        path_p = get_optimal_path(amb_start, pat_loc)
        path_h = get_optimal_path(pat_loc, target_hospital)
        
        c1, c2 = st.columns(2)
        
        # Phase 1: Patient Acquisition
        with c1:
            st.markdown("### Acquisition Phase")
            for node in path_p:
                st.write(f"Arrived at: {node}")
                requests.post(f"{BASE_URL}/step", json={"next_node": node})
                time.sleep(0.2)
        
        # Phase 2: Medical Transfer
        with c2:
            st.markdown("### Transfer Phase")
            final_obs = None
            for node in path_h:
                st.write(f"Navigating: {node}")
                step_res = requests.post(f"{BASE_URL}/step", json={"next_node": node}).json()
                final_obs = step_res["observation"]
                time.sleep(0.2)

        # Performance Analytics
        st.markdown("---")
        st.subheader("Analytics")
        m1, m2, m3 = st.columns(3)
        
        health = final_obs['patient_health']
        m1.metric("Final Vitals", f"{health}%")
        m2.metric("Nodes Visited", len(path_p) + len(path_h))
        m3.metric("Status", "SUCCESS" if health > 0 else "FAILURE")

        if health > 0:
            st.success(f"Report: Patient reached to {target_hospital}")
        else:
            st.error("Report: Patient vitals lost during transit")

    except Exception as e:
        st.error(f"Environment Error: {e}")

# Footer Credit
st.markdown("""
    <div class="custom-footer">
        Developed by Rahul 
    </div>
    """, unsafe_allow_html=True)