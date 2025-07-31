#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <chrono>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;

// Data structures
struct Point {
    double x, y;
    int demand;
    int id;
    
    Point(double x = 0, double y = 0, int demand = 0, int id = 0) 
        : x(x), y(y), demand(demand), id(id) {}
};

struct Route {
    vector<int> customers;
    double totalCost;
    int totalDemand;
    
    Route() : totalCost(0), totalDemand(0) {}
};

class VRPSolver {
private:
    vector<Point> points;
    vector<vector<double>> distanceMatrix;
    int vehicleCapacity;
    int numVehicles;
    
    double calculateDistance(const Point& p1, const Point& p2) {
        return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
    }
    
    void buildDistanceMatrix() {
        int n = points.size();
        distanceMatrix.resize(n, vector<double>(n));
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                distanceMatrix[i][j] = calculateDistance(points[i], points[j]);
            }
        }
    }
    
    double calculateRouteCost(const vector<int>& route) {
        if (route.empty()) return 0;
        
        double cost = 0;
        int lastCustomer = 0; // Start from depot
        
        for (int customer : route) {
            cost += distanceMatrix[lastCustomer][customer];
            lastCustomer = customer;
        }
        
        // Return to depot
        cost += distanceMatrix[lastCustomer][0];
        return cost;
    }
    
    int calculateRouteDemand(const vector<int>& route) {
        int demand = 0;
        for (int customer : route) {
            demand += points[customer].demand;
        }
        return demand;
    }

public:
    VRPSolver(const vector<Point>& points, int vehicleCapacity, int numVehicles) 
        : points(points), vehicleCapacity(vehicleCapacity), numVehicles(numVehicles) {
        buildDistanceMatrix();
    }
    
    // Enhanced Custom Algorithm (Clarke-Wright + 2-opt)
    vector<Route> enhancedCustomAlgorithm() {
        vector<Route> routes;
        vector<bool> visited(points.size(), false);
        visited[0] = true; // Depot is always visited
        
        // Clarke-Wright savings approach
        vector<pair<double, pair<int, int>>> savings;
        
        for (int i = 1; i < points.size(); i++) {
            for (int j = i + 1; j < points.size(); j++) {
                double saving = distanceMatrix[0][i] + distanceMatrix[0][j] - distanceMatrix[i][j];
                savings.push_back({saving, {i, j}});
            }
        }
        
        sort(savings.rbegin(), savings.rend()); // Sort by decreasing savings
        
        // Create initial routes using savings
        for (auto& saving : savings) {
            int i = saving.second.first;
            int j = saving.second.second;
            
            if (!visited[i] && !visited[j]) {
                int totalDemand = points[i].demand + points[j].demand;
                if (totalDemand <= vehicleCapacity) {
                    Route route;
                    route.customers = {i, j};
                    route.totalDemand = totalDemand;
                    route.totalCost = calculateRouteCost(route.customers);
                    routes.push_back(route);
                    visited[i] = visited[j] = true;
                }
            }
        }
        
        // Add remaining customers
        for (int i = 1; i < points.size(); i++) {
            if (!visited[i]) {
                // Try to add to existing route
                bool added = false;
                for (auto& route : routes) {
                    if (route.totalDemand + points[i].demand <= vehicleCapacity) {
                        route.customers.push_back(i);
                        route.totalDemand += points[i].demand;
                        route.totalCost = calculateRouteCost(route.customers);
                        added = true;
                        break;
                    }
                }
                
                if (!added && routes.size() < numVehicles) {
                    Route route;
                    route.customers = {i};
                    route.totalDemand = points[i].demand;
                    route.totalCost = calculateRouteCost(route.customers);
                    routes.push_back(route);
                }
            }
        }
        
        // Apply 2-opt optimization to each route
        for (auto& route : routes) {
            optimizeRoute2Opt(route);
        }
        
        return routes;
    }
    
    // 2-opt optimization for a single route
    void optimizeRoute2Opt(Route& route) {
        if (route.customers.size() < 3) return;
        
        bool improved = true;
        while (improved) {
            improved = false;
            double bestCost = calculateRouteCost(route.customers);
            
            for (int i = 0; i < route.customers.size() - 1; i++) {
                for (int j = i + 2; j < route.customers.size(); j++) {
                    // Try 2-opt swap
                    vector<int> newRoute = route.customers;
                    reverse(newRoute.begin() + i + 1, newRoute.begin() + j + 1);
                    
                    double newCost = calculateRouteCost(newRoute);
                    if (newCost < bestCost) {
                        route.customers = newRoute;
                        route.totalCost = newCost;
                        bestCost = newCost;
                        improved = true;
                        break;
                    }
                }
                if (improved) break;
            }
        }
    }
    
    // Nearest Neighbor Algorithm
    vector<Route> nearestNeighborAlgorithm() {
        vector<Route> routes;
        vector<bool> visited(points.size(), false);
        visited[0] = true; // Depot is always visited
        
        while (true) {
            Route currentRoute;
            int currentVehicle = 0;
            
            while (currentVehicle < numVehicles && currentRoute.totalDemand < vehicleCapacity) {
                int nearestCustomer = -1;
                double minDistance = 1e9;
                
                for (int i = 1; i < points.size(); i++) {
                    if (!visited[i] && currentRoute.totalDemand + points[i].demand <= vehicleCapacity) {
                        double distance = distanceMatrix[currentVehicle][i];
                        if (distance < minDistance) {
                            minDistance = distance;
                            nearestCustomer = i;
                        }
                    }
                }
                
                if (nearestCustomer == -1) break;
                
                currentRoute.customers.push_back(nearestCustomer);
                currentRoute.totalDemand += points[nearestCustomer].demand;
                visited[nearestCustomer] = true;
                currentVehicle = nearestCustomer;
            }
            
            if (currentRoute.customers.empty()) break;
            
            currentRoute.totalCost = calculateRouteCost(currentRoute.customers);
            routes.push_back(currentRoute);
        }
        
        return routes;
    }
    
    // Clarke-Wright Savings Algorithm
    vector<Route> clarkeWrightAlgorithm() {
        vector<Route> routes;
        vector<bool> visited(points.size(), false);
        visited[0] = true;
        
        // Calculate savings
        vector<pair<double, pair<int, int>>> savings;
        for (int i = 1; i < points.size(); i++) {
            for (int j = i + 1; j < points.size(); j++) {
                double saving = distanceMatrix[0][i] + distanceMatrix[0][j] - distanceMatrix[i][j];
                savings.push_back({saving, {i, j}});
            }
        }
        
        sort(savings.rbegin(), savings.rend());
        
        // Create routes based on savings
        for (auto& saving : savings) {
            int i = saving.second.first;
            int j = saving.second.second;
            
            if (!visited[i] && !visited[j]) {
                int totalDemand = points[i].demand + points[j].demand;
                if (totalDemand <= vehicleCapacity) {
                    Route route;
                    route.customers = {i, j};
                    route.totalDemand = totalDemand;
                    route.totalCost = calculateRouteCost(route.customers);
                    routes.push_back(route);
                    visited[i] = visited[j] = true;
                }
            }
        }
        
        // Add remaining customers
        for (int i = 1; i < points.size(); i++) {
            if (!visited[i]) {
                bool added = false;
                for (auto& route : routes) {
                    if (route.totalDemand + points[i].demand <= vehicleCapacity) {
                        route.customers.push_back(i);
                        route.totalDemand += points[i].demand;
                        route.totalCost = calculateRouteCost(route.customers);
                        added = true;
                        break;
                    }
                }
                
                if (!added && routes.size() < numVehicles) {
                    Route route;
                    route.customers = {i};
                    route.totalDemand = points[i].demand;
                    route.totalCost = calculateRouteCost(route.customers);
                    routes.push_back(route);
                }
            }
        }
        
        return routes;
    }
    
    // Convert routes to string for Python interface
    string routesToString(const vector<Route>& routes) {
        stringstream ss;
        ss << routes.size() << "\n";
        
        for (const auto& route : routes) {
            ss << route.totalCost << " " << route.totalDemand << " " << route.customers.size();
            for (int customer : route.customers) {
                ss << " " << customer;
            }
            ss << "\n";
        }
        
        return ss.str();
    }
};

// Read input from file
vector<Point> readInputFromFile(const string& filename, int& vehicleCapacity, int& numVehicles) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Cannot open file " << filename << endl;
        return {};
    }
    
    int numPoints;
    file >> numPoints >> vehicleCapacity >> numVehicles;
    
    vector<Point> points;
    for (int i = 0; i < numPoints; i++) {
        double x, y;
        int demand, id;
        file >> x >> y >> demand >> id;
        points.push_back(Point(x, y, demand, id));
    }
    
    file.close();
    return points;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <algorithm> <input_file>" << endl;
        cerr << "Algorithms: enhanced, nearest, clarke" << endl;
        return 1;
    }
    
    string algorithm = argv[1];
    string inputFile = argv[2];
    
    int vehicleCapacity, numVehicles;
    vector<Point> points = readInputFromFile(inputFile, vehicleCapacity, numVehicles);
    
    if (points.empty()) {
        return 1;
    }
    
    VRPSolver solver(points, vehicleCapacity, numVehicles);
    vector<Route> routes;
    
    if (algorithm == "enhanced") {
        routes = solver.enhancedCustomAlgorithm();
    } else if (algorithm == "nearest") {
        routes = solver.nearestNeighborAlgorithm();
    } else if (algorithm == "clarke") {
        routes = solver.clarkeWrightAlgorithm();
    } else {
        cerr << "Unknown algorithm: " << algorithm << endl;
        return 1;
    }
    
    cout << solver.routesToString(routes);
    return 0;
} 