import heapq

def shortest(start, end, edges):
    q = [(0,start)]
    seen=set()

    while q:
        cost,node = heapq.heappop(q)
        if node==end:
            return cost
        if node in seen: continue
        seen.add(node)
        for n,w in edges[node].items():
            heapq.heappush(q,(cost+w,n))
    return 999


def grade(obs, steps, edges):
    if obs["patient_health"] <= 0:
        return 0.0

    score = 0

    
    score += (obs["patient_health"]/100)*0.3

    
    if obs["picked"]:
        score += 0.2

    
    if "Hospital" in obs["current_node"]:
        score += 0.3

    
    opt = shortest("ISBT", obs["patient_location"], edges)
    if steps < opt * 2:
        score += 0.2

    return round(min(score,1.0),2)