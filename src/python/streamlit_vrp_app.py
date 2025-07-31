import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
import time
import math
import os
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vrp_wrapper import CppVRPWrapper

# Initialize C++ wrapper
@st.cache_resource
def get_cpp_wrapper():
    return CppVRPWrapper()

# Initialize session state
if 'customer_data' not in st.session_state:
    st.session_state.customer_data = {}

# Page configuration for deployment
st.set_page_config(
    page_title="🚚 VRP Algorithm Demo",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🚚 Vehicle Routing Problem Algorithm Demo")
st.markdown("Interactive comparison of your enhanced algorithm vs classical methods")

# Sidebar for problem settings
st.sidebar.header("Problem Settings")

# Problem parameters
num_customers = st.sidebar.slider("Number of Customers", 5, 15, 8, key="num_customers_slider")
vehicle_capacity = st.sidebar.slider("Vehicle Capacity", 20, 50, 30, key="vehicle_capacity_slider")
num_vehicles = st.sidebar.slider("Number of Vehicles", 2, 5, 3, key="num_vehicles_slider")

# Customer data input
st.sidebar.header("Customer Data")
st.sidebar.markdown("Set individual demand and location for each customer:")

# Initialize customer data if not exists
for i in range(1, num_customers + 1):
    if i not in st.session_state.customer_data:
        st.session_state.customer_data[i] = {
            'demand': random.randint(1, max(1, vehicle_capacity // 3)),
            'x': random.uniform(10, 90),
            'y': random.uniform(10, 90)
        }

# Customer data inputs
for i in range(1, num_customers + 1):
    st.sidebar.markdown(f"**Customer {i}:**")
    demand = st.sidebar.number_input(
        f"Demand",
        min_value=1, max_value=vehicle_capacity,
        value=st.session_state.customer_data.get(i, {}).get('demand', random.randint(1, max(1, vehicle_capacity // 3))),
        key=f"demand_{i}"
    )
    col1, col2 = st.sidebar.columns(2)
    with col1:
        x_coord = st.number_input(
            f"X", min_value=0.0, max_value=100.0,
            value=st.session_state.customer_data.get(i, {}).get('x', random.uniform(10, 90)),
            step=1.0, key=f"x_{i}"
        )
    with col2:
        y_coord = st.number_input(
            f"Y", min_value=0.0, max_value=100.0,
            value=st.session_state.customer_data.get(i, {}).get('y', random.uniform(10, 90)),
            step=1.0, key=f"y_{i}"
        )
    st.session_state.customer_data[i] = {'demand': demand, 'x': x_coord, 'y': y_coord}

# Random values button
if st.sidebar.button("🎲 Generate Random Values"):
    random.seed(int(time.time()))
    for i in range(1, num_customers + 1):
        st.session_state.customer_data[i] = {
            'demand': random.randint(1, max(1, vehicle_capacity // 3)),
            'x': random.uniform(10, 90),
            'y': random.uniform(10, 90)
        }
    st.rerun()

# Generate problem data
def generate_random_problem():
    points = [{'x': 50, 'y': 50, 'demand': 0}]  # Depot at center
    
    for i in range(1, num_customers + 1):
        customer_data = st.session_state.customer_data.get(i, {})
        points.append({
            'x': customer_data.get('x', random.uniform(10, 90)),
            'y': customer_data.get('y', random.uniform(10, 90)),
            'demand': customer_data.get('demand', random.randint(1, max(1, vehicle_capacity // 3)))
        })
    
    return points

# Plot routes function
def plot_routes(points, routes):
    """Create interactive route visualization"""
    fig = go.Figure()
    
    # Add depot
    fig.add_trace(go.Scatter(
        x=[points[0]['x']],
        y=[points[0]['y']],
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='star'),
        text=['Depot'],
        textposition='top center',
        name='Depot',
        showlegend=True
    ))
    
    # Add customers
    customer_x = [point['x'] for point in points[1:]]
    customer_y = [point['y'] for point in points[1:]]
    customer_text = [f'C{i}' for i in range(1, len(points))]
    
    fig.add_trace(go.Scatter(
        x=customer_x,
        y=customer_y,
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=customer_text,
        textposition='top center',
        name='Customers',
        showlegend=True
    ))
    
    # Add routes
    colors = ['red', 'green', 'blue', 'purple', 'orange', 'brown', 'pink', 'gray']
    
    for i, route in enumerate(routes):
        if route['customers']:
            route_points = [0] + route['customers'] + [0]  # Start and end at depot
            route_x = []
            route_y = []
            
            for j in route_points:
                if 0 <= j < len(points):
                    route_x.append(points[j]['x'])
                    route_y.append(points[j]['y'])
            
            if route_x and route_y:
                fig.add_trace(go.Scatter(
                    x=route_x,
                    y=route_y,
                    mode='lines+markers',
                    line=dict(width=3, color=colors[i % len(colors)]),
                    name=f'Route {i+1} (Demand: {route["totalDemand"]})',
                    showlegend=True
                ))
    
    fig.update_layout(
        title="Route Visualization",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        height=500,
        showlegend=True
    )
    
    return fig

# Problem instance display
st.header("📊 Problem Instance")
problem = generate_random_problem()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Customers", num_customers)
with col2:
    st.metric("Vehicle Capacity", vehicle_capacity)
with col3:
    st.metric("Vehicles", num_vehicles)
with col4:
    total_demand = sum(point['demand'] for point in problem[1:])  # Exclude depot
    st.metric("Total Demand", total_demand)

# Customer data table
st.subheader("Customer Data")
customer_df = pd.DataFrame([
    {
        'Customer': i,
        'Demand': st.session_state.customer_data[i]['demand'],
        'X': round(st.session_state.customer_data[i]['x'], 2),
        'Y': round(st.session_state.customer_data[i]['y'], 2)
    }
    for i in range(1, num_customers + 1)
])
st.dataframe(customer_df, use_container_width=True)

# Solve button
if st.button("🚀 Solve VRP with All Algorithms"):
    with st.spinner("Solving VRP problems..."):
        # Get C++ wrapper
        cpp_wrapper = get_cpp_wrapper()
        
        # Solve with different algorithms
        enhanced_routes = cpp_wrapper.solve_enhanced_custom(problem, vehicle_capacity, num_vehicles)
        nearest_routes = cpp_wrapper.solve_nearest_neighbor(problem, vehicle_capacity, num_vehicles)
        clarke_routes = cpp_wrapper.solve_clarke_wright(problem, vehicle_capacity, num_vehicles)
        
        # Store results
        st.session_state.problem = problem
        st.session_state.results = {
            'Enhanced Custom': {
                'routes': enhanced_routes,
                'totalCost': sum(route['totalCost'] for route in enhanced_routes),
                'numRoutes': len(enhanced_routes)
            },
            'Nearest Neighbor': {
                'routes': nearest_routes,
                'totalCost': sum(route['totalCost'] for route in nearest_routes),
                'numRoutes': len(nearest_routes)
            },
            'Clarke-Wright': {
                'routes': clarke_routes,
                'totalCost': sum(route['totalCost'] for route in clarke_routes),
                'numRoutes': len(clarke_routes)
            }
        }
    
    st.success("✅ VRP solved successfully!")

# Display results
if 'results' in st.session_state:
    st.header("🎯 Algorithm Results")
    
    # Results metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Enhanced Custom")
        fig1 = plot_routes(st.session_state.problem, st.session_state.results['Enhanced Custom']['routes'])
        st.plotly_chart(fig1, use_container_width=True, key="enhanced_custom_chart")
        st.metric("Total Cost", f"{st.session_state.results['Enhanced Custom']['totalCost']:.2f}")
        st.metric("Routes", st.session_state.results['Enhanced Custom']['numRoutes'])
    
    with col2:
        st.subheader("Nearest Neighbor")
        fig2 = plot_routes(st.session_state.problem, st.session_state.results['Nearest Neighbor']['routes'])
        st.plotly_chart(fig2, use_container_width=True, key="nearest_neighbor_chart")
        st.metric("Total Cost", f"{st.session_state.results['Nearest Neighbor']['totalCost']:.2f}")
        st.metric("Routes", st.session_state.results['Nearest Neighbor']['numRoutes'])
    
    with col3:
        st.subheader("Clarke-Wright")
        fig3 = plot_routes(st.session_state.problem, st.session_state.results['Clarke-Wright']['routes'])
        st.plotly_chart(fig3, use_container_width=True, key="clarke_wright_chart")
        st.metric("Total Cost", f"{st.session_state.results['Clarke-Wright']['totalCost']:.2f}")
        st.metric("Routes", st.session_state.results['Clarke-Wright']['numRoutes'])
    
    # Performance comparison
    st.header("📈 Performance Comparison")
    
    # Bar chart
    costs = [
        st.session_state.results['Enhanced Custom']['totalCost'],
        st.session_state.results['Nearest Neighbor']['totalCost'],
        st.session_state.results['Clarke-Wright']['totalCost']
    ]
    
    algorithms = ['Enhanced Custom', 'Nearest Neighbor', 'Clarke-Wright']
    
    fig = go.Figure(data=[
        go.Bar(
            x=algorithms,
            y=costs,
            text=[f'{cost:.2f}' for cost in costs],
            textposition='auto',
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
    ])
    
    fig.update_layout(
        title="Total Cost Comparison",
        xaxis_title="Algorithm",
        yaxis_title="Total Cost",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True, key="performance_comparison_chart")
    
    # Algorithm ranking
    st.header("🏆 Algorithm Ranking")
    
    # Sort algorithms by cost
    sorted_results = sorted(
        st.session_state.results.items(),
        key=lambda x: x[1]['totalCost']
    )
    
    medals = ['🥇', '🥈', '🥉']
    for i, (algorithm, result) in enumerate(sorted_results):
        medal = medals[i] if i < 3 else '🏅'
        st.markdown(f"{medal} **{algorithm}**: {result['totalCost']:.2f} (Cost)")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Your Enhanced VRP Algorithm Demo") 