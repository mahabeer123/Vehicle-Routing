#!/usr/bin/env python3

import math
import random
from typing import List, Dict, Tuple

class VRPAlgorithms:
    def __init__(self, points: List[Dict], vehicle_capacity: int, num_vehicles: int):
        self.points = points
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        self.distance_matrix = self._build_distance_matrix()
    
    def _build_distance_matrix(self):
        """Build distance matrix between all points"""
        n = len(self.points)
        matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = self.points[i]['x'] - self.points[j]['x']
                    dy = self.points[i]['y'] - self.points[j]['y']
                    matrix[i][j] = math.sqrt(dx*dx + dy*dy)
        
        return matrix
    
    def _calculate_route_cost(self, route: List[int]) -> float:
        """Calculate total cost of a route"""
        if not route:
            return 0
        
        cost = 0
        last_point = 0  # Start from depot
        
        for customer in route:
            cost += self.distance_matrix[last_point][customer]
            last_point = customer
        
        # Return to depot
        cost += self.distance_matrix[last_point][0]
        return cost
    
    def _calculate_route_demand(self, route: List[int]) -> int:
        """Calculate total demand of a route"""
        return sum(self.points[customer]['demand'] for customer in route)
    
    def enhanced_custom_algorithm(self):
        """Enhanced Custom Algorithm with advanced optimization"""
        routes = []
        visited = [False] * len(self.points)
        visited[0] = True
        
        # Phase 1: Create initial routes using advanced scoring
        while True:
            found_customer = False
            best_score = -1
            best_customer = -1
            best_route_index = -1
            
            # Try to add customers to existing routes
            for customer in range(1, len(self.points)):
                if visited[customer]:
                    continue
                
                for route_index in range(len(routes)):
                    route = routes[route_index]
                    
                    # Check capacity constraint
                    if route['totalDemand'] + self.points[customer]['demand'] > self.vehicle_capacity:
                        continue
                    
                    # Calculate advanced score for this customer-route combination
                    score = self._calculate_advanced_score(customer, route)
                    
                    if score > best_score:
                        best_score = score
                        best_customer = customer
                        best_route_index = route_index
                        found_customer = True
            
            # If no customer can be added to existing routes, create new route
            if not found_customer:
                for customer in range(1, len(self.points)):
                    if visited[customer]:
                        continue
                    
                    if len(routes) < self.num_vehicles:
                        score = self._calculate_advanced_score(customer, {'customers': [], 'totalCost': 0, 'totalDemand': 0})
                        
                        if score > best_score:
                            best_score = score
                            best_customer = customer
                            best_route_index = len(routes)
                            found_customer = True
            
            if not found_customer:
                break
            
            # Add the best customer to the best route
            if best_route_index == len(routes):
                # Create new route
                new_route = {
                    'customers': [best_customer],
                    'totalDemand': self.points[best_customer]['demand'],
                    'totalCost': 0
                }
                new_route['totalCost'] = self._calculate_route_cost(new_route['customers'])
                routes.append(new_route)
            else:
                # Add to existing route with optimal insertion
                best_insertion_cost = float('inf')
                best_insertion_pos = 0
                
                for pos in range(len(routes[best_route_index]['customers']) + 1):
                    new_route = routes[best_route_index]['customers'].copy()
                    new_route.insert(pos, best_customer)
                    cost = self._calculate_route_cost(new_route)
                    if cost < best_insertion_cost:
                        best_insertion_cost = cost
                        best_insertion_pos = pos
                
                routes[best_route_index]['customers'].insert(best_insertion_pos, best_customer)
                routes[best_route_index]['totalDemand'] += self.points[best_customer]['demand']
                routes[best_route_index]['totalCost'] = self._calculate_route_cost(routes[best_route_index]['customers'])
            
            visited[best_customer] = True
        
        # Phase 2: Optimize routes using 2-opt local search
        for route in routes:
            if len(route['customers']) > 2:
                route['customers'] = self._optimize_route_2opt(route['customers'])
                route['totalCost'] = self._calculate_route_cost(route['customers'])
        
        return routes
    
    def _calculate_advanced_score(self, customer: int, route: Dict) -> float:
        """Calculate advanced scoring for customer-route combination"""
        if not route['customers']:
            # For new route, calculate distance from depot
            distance = self.distance_matrix[0][customer]
            demand_ratio = self.points[customer]['demand'] / self.vehicle_capacity
            
            # Advanced scoring: balance distance, demand, and potential
            distance_factor = 1.0 / (distance + 1.0)
            demand_efficiency = 1.0 + 1.0 * demand_ratio  # Higher weight for demand
            potential_factor = 1.0  # Consider future potential
            
            return distance_factor * demand_efficiency * potential_factor
        else:
            # For existing route, find best insertion position
            best_score = -1
            
            for pos in range(len(route['customers']) + 1):
                # Calculate cost if customer inserted at this position
                insertion_cost = self._calculate_insertion_cost(customer, route['customers'], pos)
                demand_ratio = self.points[customer]['demand'] / self.vehicle_capacity
                
                # Advanced penalty system
                route_length_penalty = 1.0
                if len(route['customers']) >= 5:
                    route_length_penalty = 0.6  # Strong penalty for very long routes
                elif len(route['customers']) >= 4:
                    route_length_penalty = 0.8
                elif len(route['customers']) >= 3:
                    route_length_penalty = 0.9
                
                # Demand balancing - prefer routes closer to half capacity
                current_demand = route['totalDemand']
                new_demand = current_demand + self.points[customer]['demand']
                capacity_ratio = new_demand / self.vehicle_capacity
                balance_factor = 1.0 - abs(capacity_ratio - 0.7)  # Prefer 70% capacity
                
                # Advanced scoring formula
                distance_factor = 1.0 / (insertion_cost + 1.0)
                demand_efficiency = 1.0 + 1.0 * demand_ratio
                
                score = distance_factor * demand_efficiency * route_length_penalty * balance_factor
                
                if score > best_score:
                    best_score = score
            
            return best_score
    
    def _optimize_route_2opt(self, route: List[int]) -> List[int]:
        """Optimize route using 2-opt local search"""
        if len(route) < 3:
            return route
        
        best_cost = self._calculate_route_cost(route)
        improved = True
        
        while improved:
            improved = False
            
            for i in range(len(route) - 1):
                for j in range(i + 2, len(route)):
                    # Try 2-opt swap
                    new_route = route.copy()
                    new_route[i:j] = reversed(new_route[i:j])
                    new_cost = self._calculate_route_cost(new_route)
                    
                    if new_cost < best_cost:
                        route = new_route
                        best_cost = new_cost
                        improved = True
                        break
                if improved:
                    break
        
        return route
    
    def _calculate_insertion_cost(self, customer: int, route: List[int], position: int) -> float:
        """Calculate cost of inserting customer at specific position"""
        if not route:
            return self.distance_matrix[0][customer] + self.distance_matrix[customer][0]
        
        new_route = route.copy()
        new_route.insert(position, customer)
        return self._calculate_route_cost(new_route)
    
    def clarke_wright_algorithm(self):
        """Clarke-Wright Savings Algorithm"""
        routes = []
        visited = [False] * len(self.points)
        visited[0] = True
        
        # Calculate savings
        savings = []
        for i in range(1, len(self.points)):
            for j in range(i + 1, len(self.points)):
                saving = self.distance_matrix[0][i] + self.distance_matrix[0][j] - self.distance_matrix[i][j]
                savings.append((saving, i, j))
        
        savings.sort(reverse=True)
        
        # Create routes based on savings
        for saving, i, j in savings:
            if not visited[i] and not visited[j]:
                total_demand = self.points[i]['demand'] + self.points[j]['demand']
                if total_demand <= self.vehicle_capacity:
                    route = {'customers': [i, j], 'totalCost': 0, 'totalDemand': total_demand}
                    route['totalCost'] = self._calculate_route_cost(route['customers'])
                    routes.append(route)
                    visited[i] = visited[j] = True
        
        # Add remaining customers to existing routes or create new routes
        for i in range(1, len(self.points)):
            if not visited[i]:
                added = False
                
                # Try to add to existing routes
                for route in routes:
                    if route['totalDemand'] + self.points[i]['demand'] <= self.vehicle_capacity:
                        # Find best insertion position
                        best_cost = float('inf')
                        best_pos = 0
                        
                        for pos in range(len(route['customers']) + 1):
                            new_route = route['customers'].copy()
                            new_route.insert(pos, i)
                            cost = self._calculate_route_cost(new_route)
                            if cost < best_cost:
                                best_cost = cost
                                best_pos = pos
                        
                        route['customers'].insert(best_pos, i)
                        route['totalDemand'] += self.points[i]['demand']
                        route['totalCost'] = self._calculate_route_cost(route['customers'])
                        added = True
                        break
                
                # Create new route if couldn't add to existing
                if not added and len(routes) < self.num_vehicles:
                    route = {'customers': [i], 'totalCost': 0, 'totalDemand': self.points[i]['demand']}
                    route['totalCost'] = self._calculate_route_cost(route['customers'])
                    routes.append(route)
        
        return routes
    
    def nearest_neighbor_algorithm(self):
        """Nearest Neighbor Algorithm"""
        routes = []
        visited = [False] * len(self.points)
        visited[0] = True
        
        while True:
            current_route = []
            current_demand = 0
            current_vehicle = 0  # Start from depot
            
            while True:
                nearest_customer = -1
                min_distance = float('inf')
                
                for i in range(1, len(self.points)):
                    if not visited[i] and current_demand + self.points[i]['demand'] <= self.vehicle_capacity:
                        distance = self.distance_matrix[current_vehicle][i]
                        if distance < min_distance:
                            min_distance = distance
                            nearest_customer = i
                
                if nearest_customer == -1:
                    break
                
                current_route.append(nearest_customer)
                current_demand += self.points[nearest_customer]['demand']
                visited[nearest_customer] = True
                current_vehicle = nearest_customer
            
            if not current_route:
                break
            
            route = {'customers': current_route, 'totalCost': 0, 'totalDemand': current_demand}
            route['totalCost'] = self._calculate_route_cost(route['customers'])
            routes.append(route)
        
        return routes 