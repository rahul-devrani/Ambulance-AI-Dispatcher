import os, requests, json
from openai import OpenAI

BASE_URL = os.getenv("ENV_URL", "http://localhost:7860")
MODEL = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_BASE = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE, api_key=TOKEN)
visited_history = []

def get_llm_decision(obs):
    global visited_history
    target = obs['target_hospital'] if obs['picked'] else obs['patient_location']
    history_str = ", ".join(visited_history[-5:])

    prompt = f"""
    Ambulance GPS System:
    Current Node: {obs['current_node']}
    Neighbors: {obs['neighbors']}
    Goal: Reach {target}
    Status: {'Picked' if obs['picked'] else 'Searching'}
    Recent History: {history_str}

    Instruction: Select the neighbor that leads to the goal. 
    Crucial: DO NOT pick a neighbor from the 'Recent History' unless it's the only option.
    Return ONLY the node name.
    """
    
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "You are a smart emergency navigator."},
                      {"role": "user", "content": prompt}],
            max_tokens=15,
            temperature=0.1
        )
        action = res.choices[0].message.content.strip().split('\n')[0].replace(".", "")
        if action not in obs["neighbors"]:
            action = obs["neighbors"][0]
        
        visited_history.append(action)
        return action
    except:
        return obs["neighbors"][0]

def run_task(task, loc, sev):
    global visited_history
    visited_history = []
    print(f"[START] task={task} env=ambulance model={MODEL}")
    
    res = requests.post(f"{BASE_URL}/reset", json={"p_loc": loc, "p_sev": sev}).json()
    obs = res["observation"]
    
    done, steps, rewards = False, 0, []
    while not done and steps < 50:
        action = get_llm_decision(obs)
        r = requests.post(f"{BASE_URL}/step", json={"next_node": action}).json()
        
        obs, reward, done = r["observation"], r["reward"], r["done"]
        steps += 1
        rewards.append(reward)
        print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    success = obs['picked'] and obs['current_node'] == obs['target_hospital'] and obs['patient_health'] > 0
    score = 1.0 if success else (obs['patient_health'] / 100.0)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={','.join([f'{r:.2f}' for r in rewards])}")

if __name__ == "__main__":
    run_task("easy", "Saharanpur Chowk", "Stable")
    run_task("medium", "Ballupur", "Stable")
    run_task("hard", "Bhaniyawala", "Critical")