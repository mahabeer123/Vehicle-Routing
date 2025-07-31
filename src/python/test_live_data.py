#!/usr/bin/env python3

from vrp_algorithms import VRPAlgorithms

# Your current live data
points = [
    {'x': 50.0, 'y': 50.0, 'demand': 0},      # Depot
    {'x': 46.43, 'y': 58.86, 'demand': 3},    # Customer 1
    {'x': 63.26, 'y': 75.16, 'demand': 1},    # Customer 2
    {'x': 73.75, 'y': 36.65, 'demand': 6},    # Customer 3
    {'x': 35.37, 'y': 48.24, 'demand': 1},    # Customer 4
    {'x': 50.44, 'y': 40.31, 'demand': 4},    # Customer 5
    {'x': 52.82, 'y': 50.78, 'demand': 10},   # Customer 6
    {'x': 12.10, 'y': 42.67, 'demand': 2},    # Customer 7
    {'x': 89.99, 'y': 49.64, 'demand': 5}     # Customer 8
]

solver = VRPAlgorithms(points, 30, 3)

print("=== LIVE DATA ANALYSIS ===")
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