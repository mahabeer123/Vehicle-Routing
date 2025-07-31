# 🚚 Vehicle Routing Problem (VRP) Algorithm Demo

An interactive web application that demonstrates and compares different algorithms for solving the Capacitated Vehicle Routing Problem (CVRP).

## 🎯 Project Overview

This project implements and compares three VRP algorithms:
- **Enhanced Custom Algorithm**: Combines Clarke-Wright savings with 2-opt optimization
- **Nearest Neighbor**: Classical greedy approach
- **Clarke-Wright**: Classical savings-based algorithm

## 🏗️ Architecture

### **C++ Core Algorithms** ⚡
- **High-performance algorithms** implemented in C++
- **Optimized for speed** and memory efficiency
- **Advanced data structures** and algorithms
- **Compiled with O2 optimization** for maximum performance

### **Python Web Interface** 🌐
- **Streamlit** for interactive web interface
- **Plotly** for dynamic visualizations
- **Pandas** for data handling
- **Clean separation** between computation and presentation

## 📁 Project Structure

```
Vehicle-Routing/
├── src/
│   ├── cpp/
│   │   ├── vrp_solver.cpp      # C++ core algorithms
│   │   └── vrp_solver          # Compiled executable
│   └── python/
│       ├── vrp_wrapper.py      # Python-C++ interface
│       └── streamlit_vrp_app.py # Main Streamlit application
├── docs/
│   └── DEPLOYMENT.md           # Deployment guide
├── examples/                   # Example data and tests
├── requirements.txt            # Python dependencies
├── runtime.txt                # Python version specification
├── Procfile                   # Heroku deployment
├── setup.sh                   # Heroku setup script
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## ✨ Features

- **Interactive Web Interface**: Built with Streamlit for easy visualization
- **User-Defined Problems**: Set custom customer demands and locations
- **Real-Time Comparison**: Compare algorithm performance instantly
- **Visual Route Display**: Interactive maps showing optimal routes
- **Performance Metrics**: Cost analysis and algorithm ranking
- **Random Problem Generation**: Quick testing with random data
- **C++ Performance**: Fast algorithm execution with compiled code

## 🚀 Quick Start

### Prerequisites
```bash
# C++ compiler (GCC/Clang)
g++ --version

# Python dependencies
pip install streamlit plotly pandas
```

### Run the Application
```bash
# Compile C++ algorithms
cd src/cpp
g++ -std=c++17 -O2 vrp_solver.cpp -o vrp_solver

# Run Streamlit app
cd ../python
streamlit run streamlit_vrp_app.py
```

The app will open at `http://localhost:8501`

## 📊 How to Use

1. **Set Problem Parameters**:
   - Number of customers (5-15)
   - Vehicle capacity (20-50)
   - Number of vehicles (2-5)

2. **Configure Customer Data**:
   - Set individual demand for each customer
   - Set X,Y coordinates for customer locations
   - Use "🎲 Generate Random Values" for quick testing

3. **Solve and Compare**:
   - Click "🚀 Solve VRP with All Algorithms"
   - View route visualizations for each algorithm
   - Compare performance metrics
   - See algorithm ranking

## 🧠 Algorithm Details

### Enhanced Custom Algorithm
- **Approach**: Hybrid savings + multi-factor scoring with demand ratio optimization
- **Formula**: Score = (1/distance) × (1 + 0.5 × demand_ratio) × route_penalty
- **Unique Features**: 
  - Savings-based initial route formation for pairs
  - Multi-factor scoring for customer insertion
  - Route length penalty to prevent overly long routes
  - 2-opt local search improvement
- **Implementation**: C++ with O2 optimization
- **Advantage**: Combines proven savings approach with innovative scoring
- **Performance**: Competitive with classical methods while being unique

### Nearest Neighbor Algorithm
- **Approach**: Greedy selection of nearest unvisited customer
- **Implementation**: C++ with optimized data structures
- **Complexity**: O(n²)
- **Use Case**: Fast baseline solution

### Clarke-Wright Algorithm
- **Approach**: Savings-based route merging
- **Implementation**: C++ with efficient sorting
- **Complexity**: O(n²log n)
- **Use Case**: Classical benchmark algorithm

## 🛠️ Technical Implementation

### C++ Core Features
- **Modern C++17**: Latest language features
- **STL Containers**: Efficient data structures
- **O2 Optimization**: Maximum performance
- **Memory Efficient**: Minimal memory footprint
- **Cross-platform**: Works on Windows, macOS, Linux

### Python Interface Features
- **Streamlit**: Modern web framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Subprocess**: C++ integration
- **Error Handling**: Graceful fallbacks

## 🎯 Use Cases

- **Educational**: Learn about VRP algorithms
- **Research**: Compare algorithm performance
- **Interview Preparation**: Demonstrate algorithm knowledge
- **Portfolio**: Showcase optimization skills
- **Performance Testing**: Benchmark algorithm efficiency

## 📈 Performance Metrics

The application tracks:
- **Total Cost**: Sum of all route distances
- **Number of Routes**: Routes created by each algorithm
- **Algorithm Ranking**: Performance comparison with medals
- **Execution Time**: C++ vs Python performance

## 🔧 Customization

### Adding New Algorithms
1. Implement algorithm in `src/cpp/vrp_solver.cpp`
2. Add to `src/python/vrp_wrapper.py` interface
3. Update Streamlit app to use new algorithm

### Modifying Problem Constraints
- Edit capacity constraints in C++ algorithms
- Adjust distance calculations in `VRPSolver` class
- Modify customer data generation in Python

## 🚀 Deployment

### Local Deployment
```bash
streamlit run src/python/streamlit_vrp_app.py
```

### Cloud Deployment
1. **Streamlit Cloud**:
   - Push to GitHub
   - Connect repository to Streamlit Cloud
   - Deploy automatically

2. **Heroku**:
   - Add `setup.sh` and `Procfile`
   - Deploy using Heroku CLI

3. **Railway**:
   - Connect GitHub repository
   - Automatic deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Mahabeer Patnaik**
- Computer Science & Engineering student
- Specialization in Algorithms & Optimization

## 🙏 Acknowledgments

- Streamlit team for the excellent web framework
- Plotly for interactive visualizations
- C++ community for optimization techniques
- Academic community for VRP algorithm research

---

**Built with ❤️ for algorithm optimization and education** 