#!/usr/bin/env python3

from vrp_algorithms import VRPAlgorithms

# Your current data
points = [
    {'x': 50.0, 'y': 50.0, 'demand': 0},      # Depot
    {'x': 79.58, 'y': 66.67, 'demand': 6},    # Customer 1
    {'x': 23.91, 'y': 79.84, 'demand': 4},    # Customer 2
    {'x': 42.89, 'y': 25.83, 'demand': 7},    # Customer 3
    {'x': 33.42, 'y': 34.14, 'demand': 6},    # Customer 4
    {'x': 69.43, 'y': 86.10, 'demand': 6},    # Customer 5
    {'x': 54.91, 'y': 87.73, 'demand': 1},    # Customer 6
    {'x': 67.08, 'y': 86.73, 'demand': 5},    # Customer 7
    {'x': 62.57, 'y': 26.89, 'demand': 3}     # Customer 8
]

solver = VRPAlgorithms(points, 30, 3)

print("=== DETAILED ALGORITHM ANALYSIS ===")
print(f"Total demand: {sum(p['demand'] for p in points[1:])}")
print(f"Vehicle capacity: 30")
print(f"Number of vehicles: 3")

print("\n=== Enhanced Custom ===")
enhanced = solver.enhanced_custom_algorithm()
enhanced_cost = sum(route['totalCost'] for route in enhanced)
print(f"Routes: {len(enhanced)}")
for i, route in enumerate(enhanced):
    print(f"  Route {i+1}: {route['customers']} - Cost: {route['totalCost']:.2f}, Demand: {route['totalDemand']}")
print(f"Total Cost: {enhanced_cost:.2f}")

print("\n=== Clarke-Wright ===")
clarke = solver.clarke_wright_algorithm()
clarke_cost = sum(route['totalCost'] for route in clarke)
print(f"Routes: {len(clarke)}")
for i, route in enumerate(clarke):
    print(f"  Route {i+1}: {route['customers']} - Cost: {route['totalCost']:.2f}, Demand: {route['totalDemand']}")
print(f"Total Cost: {clarke_cost:.2f}")

print("\n=== Nearest Neighbor ===")
nearest = solver.nearest_neighbor_algorithm()
nearest_cost = sum(route['totalCost'] for route in nearest)
print(f"Routes: {len(nearest)}")
for i, route in enumerate(nearest):
    print(f"  Route {i+1}: {route['customers']} - Cost: {route['totalCost']:.2f}, Demand: {route['totalDemand']}")
print(f"Total Cost: {nearest_cost:.2f}")

print(f"\n=== PERFORMANCE ANALYSIS ===")
print(f"Enhanced Custom: {enhanced_cost:.2f}")
print(f"Clarke-Wright: {clarke_cost:.2f}")
print(f"Nearest Neighbor: {nearest_cost:.2f}")

if enhanced_cost == clarke_cost:
    print("⚠️ WARNING: Enhanced Custom and Clarke-Wright are identical!")
    print("This means the algorithms are producing the same routes.")
else:
    print("✅ Enhanced Custom is different from Clarke-Wright")

if enhanced_cost <= clarke_cost:
    print("✅ Enhanced Custom is better than or equal to Clarke-Wright")
else:
    print("❌ Enhanced Custom is worse than Clarke-Wright")

if clarke_cost <= nearest_cost:
    print("✅ Clarke-Wright is better than or equal to Nearest Neighbor")
else:
    print("❌ Clarke-Wright is worse than Nearest Neighbor") 