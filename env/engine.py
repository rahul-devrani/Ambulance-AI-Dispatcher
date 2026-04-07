import random
from env.map_loader import load_map
from env.traffic_sim import get_traffic_multiplier

class AmbulanceEngine:
    def __init__(self, map_name="dehradun_map.json"):
        self.nodes, self.edges = load_map(map_name)
        self.hospitals = [n for n, v in self.nodes.items() if v["type"] == "hospital"]
        self.reset()

    def reset(self, p_loc=None, p_sev=None):
        self.current_node = "ISBT"
        self.patient_location = p_loc or "Bhaniyawala"
        self.severity = p_sev or "Critical"
        self.patient_health = 100.0
        self.patient_picked = False
        self.target_hospital = self._select_best_hospital()
        self.done = False
        return self._obs("Start")

    def _select_best_hospital(self):
        # Professional Triage: Critical patients must go to ICU
        icu_hospitals = [h for h in self.hospitals if self.nodes[h].get("has_icu")]
        if self.severity == "Critical" and icu_hospitals:
            return icu_hospitals[0] 
        return self.hospitals[0]

    def step(self, next_node: str):
        if self.done: return self._obs("Already Ended"), 0.0, True
        
        if next_node not in self.edges.get(self.current_node, {}):
            return self._obs("Invalid Route"), -1.0, False

        mult, traffic = get_traffic_multiplier()
        cost = self.edges[self.current_node][next_node] * mult
        
        self.current_node = next_node
        
        # Decay
        decay_rate = 1.2 if self.severity == "Critical" else 0.5
        self.patient_health = max(0, round(self.patient_health - (cost * decay_rate), 2))

        if self.patient_health <= 0:
            self.done = True
            return self._obs("Patient Lost"), -10.0, True

        # Reward for Pickup
        if not self.patient_picked and self.current_node == self.patient_location:
            self.patient_picked = True
            return self._obs("Patient Secured"), 5.0, False

        # Reward for Delivery
        if self.patient_picked and self.current_node == self.target_hospital:
            self.done = True
            return self._obs("Success Finished"), 20.0, True

        return self._obs(f"Moving ({traffic})"), -0.05 * cost, False

    def _obs(self, msg):
        return {
            "current_node": self.current_node,
            "neighbors": list(self.edges.get(self.current_node, {}).keys()),
            "patient_location": self.patient_location,
            "target_hospital": self.target_hospital,
            "patient_health": self.patient_health,
            "patient_severity": self.severity,
            "phase": "transport" if self.patient_picked else "pickup",
            "message": msg
        }