# Ambulance AI Rescue Pro

A real-world OpenEnv reinforcement learning environment for ambulance routing in Dehradun. The agent must navigate a city graph, pick up a patient, and deliver them to the correct hospital before their health reaches zero.

Objective
- Reach patient location
- Pick up the patient
- Deliver to the appropriate hospital
- Maximize patient survival

Features
- Real map-based routing using Dehradun graph
- Health decay based on patient severity
- LLM-based decision making (OpenAI client compliant)
- Loop prevention using recent history tracking
- Reward-based learning environment
- Streamlit UI for visualization and manual interaction

API Endpoints
- POST /reset → Initialize environment
- POST /step → Execute action
- GET /state → Get current state

Tasks
- Easy: Stable patient, short route
- Medium: Moderate complexity
- Hard: Critical patient, long route

Reward Design
- Movement: Negative cost
- Patient pickup: +30
- Successful delivery: +100
- Invalid move: -10
- Patient death / timeout: -100


Inference:
python inference.py

Streamlit UI:
streamlit run app_ui.py
