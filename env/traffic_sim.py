import random

def get_traffic_multiplier():
    # Real world variability simulation
    traffic_conditions = {
        ("low", 1.0, 0.4),      # 40% chance
        ("moderate", 1.8, 0.3), # 30% chance
        ("heavy", 3.5, 0.2),    # 20% chance
        ("jam", 6.0, 0.1)       # 10% chance
    }
    
    choices = [c[0] for c in traffic_conditions]
    weights = [c[2] for c in traffic_conditions]
    multipliers = {c[0]: c[1] for c in traffic_conditions}
    
    selected_traffic = random.choices(choices, weights=weights, k=1)[0]
    return multipliers[selected_traffic], selected_traffic