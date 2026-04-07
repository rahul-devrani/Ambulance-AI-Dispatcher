import os
import asyncio
import requests
import heapq
import json

# config
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")
BASE_URL = "http://localhost:7860"

def get_path(start, end, edges):
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            path = path + [node]
            if node == end: return path[1:]
            seen.add(node)
            for n, w in edges.get(node, {}).items():
                heapq.heappush(queue, (cost + w, n, path))
    return []

async def main():
    print(f"[START] task=emergency_rescue_hard env=ambulance model={MODEL_NAME}")
    
    try:
        with open("data/dehradun_map.json") as f:
            edges = json.load(f)["edges"]

        # Reset Env
        res = requests.post(f"{BASE_URL}/reset", json={"p_loc": "Bhaniyawala", "p_sev": "Critical"}).json()
        obs = res["observation"]
        
        rewards = []
        step_count = 0
        done = False

        # Phase 1: Go to Patient -> Phase 2: Go to Hospital
        targets = [obs['patient_location'], obs['target_hospital']]
        
        for target in targets:
            if obs['current_node'] == target: continue
            path = get_path(obs['current_node'], target, edges)
            
            for move in path:
                step_count += 1
                step_res = requests.post(f"{BASE_URL}/step", json={"next_node": move}).json()
                obs, reward, done = step_res["observation"], step_res["reward"], step_res["done"]
                rewards.append(reward)
                
                print(f"[STEP] step={step_count} action={move} reward={reward:.2f} done={str(done).lower()} error=null")
                if done: break
            if done: break

        # Final Scoring
        success_status = obs["patient_health"] > 0 and done
        success = "true" if success_status else "false"
        
        # Grading Logic: 1.0 for success, otherwise based on health
        score = 1.0 if success_status else (obs["patient_health"] / 100.0)
        
        reward_list_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={success} steps={step_count} score={score:.2f} rewards={reward_list_str}")

    except Exception as e:
        print(f"[END] success=false steps=0 score=0.00 rewards=0.00")

if __name__ == "__main__":
    asyncio.run(main())