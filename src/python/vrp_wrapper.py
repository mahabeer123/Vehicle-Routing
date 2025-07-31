import subprocess
import json
import tempfile
import os
import sys

class CppVRPWrapper:
    def __init__(self):
        self.cpp_executable = None
        self._compile_cpp()
    
    def _compile_cpp(self):
        """Compile the C++ VRP solver"""
        try:
            # Compile the C++ code
            result = subprocess.run([
                'g++', '-std=c++17', '-O2', 
                'vrp_solver.cpp', '-o', 'vrp_solver'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.cpp_executable = './vrp_solver'
                print("✅ C++ VRP solver compiled successfully")
            else:
                print(f"❌ Compilation failed: {result.stderr}")
                self.cpp_executable = None
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            self.cpp_executable = None
    
    def _create_input_file(self, points, vehicle_capacity, num_vehicles):
        """Create input file for C++ solver"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            # Write problem parameters
            f.write(f"{len(points)} {vehicle_capacity} {num_vehicles}\n")
            
            # Write points (depot first, then customers)
            for i, point in enumerate(points):
                f.write(f"{point['x']} {point['y']} {point['demand']} {i}\n")
            
            return f.name
    
    def _parse_output(self, output):
        """Parse C++ solver output"""
        lines = output.strip().split('\n')
        if not lines:
            return []
        
        num_routes = int(lines[0])
        routes = []
        
        for i in range(1, num_routes + 1):
            if i >= len(lines):
                break
                
            parts = lines[i].split()
            if len(parts) < 3:
                continue
                
            total_cost = float(parts[0])
            total_demand = int(parts[1])
            num_customers = int(parts[2])
            
            customers = []
            if len(parts) > 3:
                customers = [int(x) for x in parts[3:3+num_customers]]
            
            routes.append({
                'customers': customers,
                'totalCost': total_cost,
                'totalDemand': total_demand
            })
        
        return routes
    
    def solve_enhanced_custom(self, points, vehicle_capacity, num_vehicles):
        """Solve using Enhanced Custom Algorithm (C++)"""
        if not self.cpp_executable:
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "enhanced")
        
        try:
            input_file = self._create_input_file(points, vehicle_capacity, num_vehicles)
            
            # Run C++ solver with enhanced algorithm
            result = subprocess.run([
                self.cpp_executable, 'enhanced', input_file
            ], capture_output=True, text=True, timeout=30)
            
            os.unlink(input_file)  # Clean up
            
            if result.returncode == 0:
                return self._parse_output(result.stdout)
            else:
                print(f"❌ C++ solver error: {result.stderr}")
                return self._fallback_solve(points, vehicle_capacity, num_vehicles, "enhanced")
                
        except Exception as e:
            print(f"❌ C++ solver exception: {e}")
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "enhanced")
    
    def solve_nearest_neighbor(self, points, vehicle_capacity, num_vehicles):
        """Solve using Nearest Neighbor Algorithm (C++)"""
        if not self.cpp_executable:
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "nearest")
        
        try:
            input_file = self._create_input_file(points, vehicle_capacity, num_vehicles)
            
            # Run C++ solver with nearest neighbor algorithm
            result = subprocess.run([
                self.cpp_executable, 'nearest', input_file
            ], capture_output=True, text=True, timeout=30)
            
            os.unlink(input_file)  # Clean up
            
            if result.returncode == 0:
                return self._parse_output(result.stdout)
            else:
                print(f"❌ C++ solver error: {result.stderr}")
                return self._fallback_solve(points, vehicle_capacity, num_vehicles, "nearest")
                
        except Exception as e:
            print(f"❌ C++ solver exception: {e}")
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "nearest")
    
    def solve_clarke_wright(self, points, vehicle_capacity, num_vehicles):
        """Solve using Clarke-Wright Algorithm (C++)"""
        if not self.cpp_executable:
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "clarke")
        
        try:
            input_file = self._create_input_file(points, vehicle_capacity, num_vehicles)
            
            # Run C++ solver with Clarke-Wright algorithm
            result = subprocess.run([
                self.cpp_executable, 'clarke', input_file
            ], capture_output=True, text=True, timeout=30)
            
            os.unlink(input_file)  # Clean up
            
            if result.returncode == 0:
                return self._parse_output(result.stdout)
            else:
                print(f"❌ C++ solver error: {result.stderr}")
                return self._fallback_solve(points, vehicle_capacity, num_vehicles, "clarke")
                
        except Exception as e:
            print(f"❌ C++ solver exception: {e}")
            return self._fallback_solve(points, vehicle_capacity, num_vehicles, "clarke")
    
    def _fallback_solve(self, points, vehicle_capacity, num_vehicles, algorithm):
        """Fallback to Python implementation if C++ fails"""
        print(f"⚠️ Using Python fallback for {algorithm} algorithm")
        
        # Import the Python implementation from the existing app
        from streamlit_vrp_app import VRPAlgorithm
        
        solver = VRPAlgorithm(points, vehicle_capacity, num_vehicles)
        
        if algorithm == "enhanced":
            return solver.enhanced_custom_algorithm()
        elif algorithm == "nearest":
            return solver.nearest_neighbor_algorithm()
        elif algorithm == "clarke":
            return solver.clarke_wright_algorithm()
        else:
            return []

# Test the wrapper
if __name__ == "__main__":
    wrapper = CppVRPWrapper()
    
    # Test data
    points = [
        {'x': 0, 'y': 0, 'demand': 0},      # Depot
        {'x': 10, 'y': 10, 'demand': 5},
        {'x': 20, 'y': 20, 'demand': 3},
        {'x': 30, 'y': 30, 'demand': 7},
        {'x': 40, 'y': 40, 'demand': 4}
    ]
    
    print("Testing C++ VRP Wrapper:")
    print("Enhanced Custom:", wrapper.solve_enhanced_custom(points, 20, 2))
    print("Nearest Neighbor:", wrapper.solve_nearest_neighbor(points, 20, 2))
    print("Clarke-Wright:", wrapper.solve_clarke_wright(points, 20, 2)) 