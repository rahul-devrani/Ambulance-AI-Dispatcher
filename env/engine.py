import random
from env.map_loader import load_map

class AmbulanceEngine:
    def __init__(self):
        self.nodes, self.edges = load_map()
        self.hospitals = [n for n,v in self.nodes.items() if v["type"]=="hospital"]

    def reset(self, p_loc=None, p_sev=None):
        random.seed(42)
        self.current_node = "ISBT"
        self.patient_location = p_loc or "Bhaniyawala"
        self.severity = p_sev or "Critical"
        self.patient_health = 100.0
        self.picked = False
        self.steps = 0
        self.done = False
        
        self.target_hospital = "Max Hospital" if self.severity == "Critical" else "Doon Hospital"
        return self._obs("reset")

    def step(self, next_node):
        if self.done: return self._obs("done"), 0.0, True
        self.steps += 1
        
        if next_node not in self.edges.get(self.current_node, {}):
            return self._obs("invalid move"), -10.0, False

        cost = self.edges[self.current_node][next_node]
        self.current_node = next_node
        
        decay = 1.6 if self.severity == "Critical" else 0.5
        self.patient_health = max(0, self.patient_health - (cost * decay))
        
        reward = -1.0 * cost 
        
        if not self.picked and self.current_node == self.patient_location:
            self.picked = True
            reward += 30.0
        
        if self.picked and self.current_node == self.target_hospital:
            self.done = True
            reward += 100.0
        elif self.patient_health <= 0 or self.steps > 45:
            self.done = True
            reward -= 100.0

        return self._obs("step"), float(reward), bool(self.done)

    def _obs(self, msg):
        return {
            "current_node": self.current_node,
            "neighbors": list(self.edges.get(self.current_node, {}).keys()),
            "patient_location": self.patient_location,
            "target_hospital": self.target_hospital,
            "patient_health": round(self.patient_health, 2),
            "severity": self.severity,
            "picked": self.picked,
            "steps": self.steps,
            "message": msg
        }