# Ambulance AI Dispatcher
The project focuses on optimizing ambulance routing in Dehradun based on patient severity, road connectivity, and hospital resources.

## Project Overview
The system simulates an emergency response scenario where an agent must navigate a city graph to rescue a patient and deliver them to the most suitable medical facility before their health vitals drop to zero.

## Features
- **City Graph:** 44 nodes representing Dehradun locations and 12 hospitals.
- **Dynamic Triage:** System logic differentiates between 'Stable' and 'Critical' patients.
- **Smart Routing:** Uses Dijkstra's algorithm for optimal pathfinding.
- **Live Dashboard:** Professional Streamlit UI for monitoring and manual mission control.

##  Folder Structure
- `data/`: City map data (`dehradun_map.json`).
- `env/`: Core engine logic and environment models.
- `server/`: FastAPI server for OpenEnv compatibility.
- `app_ui.py`: Streamlit-based user interface.
- `inference.py`: Benchmarking and evaluation script.
- `Dockerfile`: Deployment configuration for Hugging Face Spaces.

##  How to Run

### 1. Start Environment Server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860


```bash
streamlit run app_ui.py


```bash
python inference.py
