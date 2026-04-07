 # Euclidean distance for internal logic

import math

def calculate_crow_fly_distance(coords1, coords2):
    return math.sqrt((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2)