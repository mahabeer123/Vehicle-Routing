#!/usr/bin/env python3

from vrp_wrapper import CppVRPWrapper

# Your current data
points = [
    {'x': 50.0, 'y': 50.0, 'demand': 0},      # Depot
    {'x': 40.38, 'y': 20.31, 'demand': 6},    # Customer 1
    {'x': 82.70, 'y': 13.73, 'demand': 10},   # Customer 2
    {'x': 44.18, 'y': 52.84, 'demand': 9},    # Customer 3
    {'x': 22.03, 'y': 76.85, 'demand': 6},    # Customer 4
    {'x': 22.96, 'y': 53.39, 'demand': 2},    # Customer 5
    {'x': 23.12, 'y': 23.63, 'demand': 5},    # Customer 6
    {'x': 16.78, 'y': 48.27, 'demand': 5},    # Customer 7
    {'x': 78.93, 'y': 64.08, 'demand': 8}     # Customer 8
]

wrapper = CppVRPWrapper()

print("Testing with your current data:")
print("Enhanced Custom:", wrapper.solve_enhanced_custom(points, 30, 3))
print("Clarke-Wright:", wrapper.solve_clarke_wright(points, 30, 3))
print("Nearest Neighbor:", wrapper.solve_nearest_neighbor(points, 30, 3)) 