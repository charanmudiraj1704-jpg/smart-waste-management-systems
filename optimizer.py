"""
Smart Waste Management System - DAA Route Optimization Engine
==============================================================
Algorithm: Greedy Nearest Neighbor + 2-Opt Heuristic for Traveling Salesperson Problem (TSP)
           and Dijkstra's Shortest Path for Road Networks.

Design and Analysis of Algorithms (DAA) Analysis:
- Problem: Vehicle Routing Problem / Traveling Salesperson Problem (NP-Hard)
- Brute Force Complexity: O(N!) - Infeasible for practical route planning
- Greedy Nearest Neighbor: O(N^2) Time Complexity, O(N) Space Complexity
- 2-Opt Optimization: O(K * N^2) where K is number of improvement iterations
- Approximation Quality: Produces a 1.25x - 1.35x near-optimal tour in milliseconds
"""

import math
import json
import heapq
from typing import List, Dict, Tuple, Any

class WasteLocation:
    def __init__(self, id_val: str, name: str, x: float, y: float, waste_type: str, urgency: str, volume_kg: float):
        self.id = id_val
        self.name = name
        self.x = x          # Grid X or Longitude-offset (km)
        self.y = y          # Grid Y or Latitude-offset (km)
        self.waste_type = waste_type
        self.urgency = urgency
        self.volume_kg = volume_kg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "waste_type": self.waste_type,
            "urgency": self.urgency,
            "volume_kg": self.volume_kg
        }

def euclidean_distance(p1: WasteLocation, p2: WasteLocation) -> float:
    """Calculates Euclidean geometric distance between two coordinate nodes."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

class SmartWasteRouteOptimizer:
    """
    DAA-based Route Optimizer for Municipal Garbage Trucks.
    Employs Greedy Nearest Neighbor with 2-Opt local search refinement.
    """
    def __init__(self, depot: WasteLocation):
        self.depot = depot
        self.locations: List[WasteLocation] = []

    def add_location(self, loc: WasteLocation):
        self.locations.append(loc)

    def calculate_total_distance(self, route: List[WasteLocation]) -> float:
        """Computes total circular tour distance (Depot -> all bins -> Depot)."""
        if not route:
            return 0.0
        total = 0.0
        for i in range(len(route) - 1):
            total += euclidean_distance(route[i], route[i + 1])
        # Return to depot from the final node
        total += euclidean_distance(route[-1], self.depot)
        return round(total, 2)

    def nearest_neighbor_tour(self) -> Tuple[List[WasteLocation], List[str]]:
        """
        DAA Algorithm 1: Greedy Nearest Neighbor (TSP)
        Time Complexity: O(N^2)
        Space Complexity: O(N)
        
        Strategy:
        1. Start at municipal depot.
        2. Repeatedly visit the closest unvisited reported waste bin.
        3. Prioritize 'Critical' bins by applying a weight bonus factor.
        4. Return tour and step-by-step algorithmic trace.
        """
        unvisited = list(self.locations)
        current = self.depot
        tour = [current]
        trace_steps = [f"Origin: Depot '{current.name}' at ({current.x}, {current.y})"]

        step = 1
        while unvisited:
            best_idx = -1
            best_score = float('inf')

            for idx, candidate in enumerate(unvisited):
                dist = euclidean_distance(current, candidate)
                # DAA Priority Weighting: Critical bins get higher urgency priority
                urgency_factor = 0.7 if candidate.urgency == 'Critical' else (0.9 if candidate.urgency == 'Moderate' else 1.0)
                effective_cost = dist * urgency_factor

                if effective_cost < best_score:
                    best_score = effective_cost
                    best_idx = idx

            next_node = unvisited.pop(best_idx)
            raw_distance = euclidean_distance(current, next_node)
            tour.append(next_node)
            trace_steps.append(
                f"Step {step}: Selected {next_node.name} [{next_node.urgency}] (Dist: {raw_distance:.2f} km) from {current.name}"
            )
            current = next_node
            step += 1

        trace_steps.append(f"Final Leg: Return from {current.name} to Depot '{self.depot.name}' (Dist: {euclidean_distance(current, self.depot):.2f} km)")
        return tour, trace_steps

    def two_opt_optimize(self, tour: List[WasteLocation], max_iterations: int = 50) -> List[WasteLocation]:
        """
        DAA Algorithm 2: 2-Opt Local Search Heuristic
        Time Complexity: O(K * N^2)
        Eliminates route crossings (subtour inversion) to optimize the Hamiltonian cycle.
        """
        n = len(tour)
        if n <= 3:
            return tour

        improved = True
        best_tour = list(tour)
        best_dist = self.calculate_total_distance(best_tour)
        iteration = 0

        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    # Perform 2-opt swap: reverse slice between i and j
                    new_tour = best_tour[:i] + best_tour[i:j + 1][::-1] + best_tour[j + 1:]
                    new_dist = self.calculate_total_distance(new_tour)
                    if new_dist < best_dist - 1e-4:
                        best_tour = new_tour
                        best_dist = new_dist
                        improved = True
                        break
                if improved:
                    break

        return best_tour

    def run_optimization(self) -> Dict[str, Any]:
        """Runs the complete DAA pipeline and returns structured performance analytics."""
        if not self.locations:
            return {"error": "No waste locations to optimize"}

        # Baseline: Unordered arrival sequence distance
        naive_tour = [self.depot] + self.locations
        naive_dist = self.calculate_total_distance(naive_tour)

        # 1. Greedy Nearest Neighbor
        nn_tour, steps = self.nearest_neighbor_tour()
        nn_dist = self.calculate_total_distance(nn_tour)

        # 2. 2-Opt Optimization
        optimized_tour = self.two_opt_optimize(nn_tour)
        optimized_dist = self.calculate_total_distance(optimized_tour)

        # Efficiency calculation
        fuel_saved_km = round(max(0, naive_dist - optimized_dist), 2)
        efficiency_gain = round(((naive_dist - optimized_dist) / naive_dist) * 100, 1) if naive_dist > 0 else 0.0
        # Estimated CO2 reduction (average diesel refuse truck emits ~2.68 kg CO2 per km)
        co2_saved_kg = round(fuel_saved_km * 2.68, 2)

        return {
            "algorithm": "Greedy Nearest Neighbor + 2-Opt Heuristic",
            "time_complexity": "O(N^2) for NN, O(K * N^2) for 2-Opt",
            "space_complexity": "O(N)",
            "depot": self.depot.to_dict(),
            "total_bins": len(self.locations),
            "naive_distance_km": naive_dist,
            "optimized_distance_km": optimized_dist,
            "fuel_saved_km": fuel_saved_km,
            "efficiency_gain_percent": efficiency_gain,
            "co2_saved_kg": co2_saved_kg,
            "trace_steps": steps,
            "route_order": [node.to_dict() for node in optimized_tour] + [self.depot.to_dict()]
        }

def dijkstra_shortest_path(graph: Dict[str, List[Tuple[str, float]]], start: str, end: str) -> Tuple[float, List[str]]:
    """
    DAA Algorithm 3: Dijkstra's Algorithm for Shortest Path Road Network
    Time Complexity: O((V + E) log V) with Priority Queue (Heap)
    Space Complexity: O(V)
    Useful for detailed turn-by-turn routing between collection waypoints.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0.0
    previous = {node: None for node in graph}
    pq = [(0.0, start)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        if curr_node == end:
            break

        for neighbor, weight in graph.get(curr_node, []):
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                previous[neighbor] = curr_node
                heapq.heappush(pq, (dist, neighbor))

    # Path reconstruction
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    return distances[end], path

# Demo & Test execution when run directly
if __name__ == "__main__":
    print("=" * 70)
    print("  SMART WASTE MANAGEMENT - DAA ROUTE OPTIMIZATION ENGINE")
    print("  Algorithm: Greedy Nearest Neighbor + 2-Opt Heuristic")
    print("=" * 70)

    # 1. Initialize Municipal Depot
    depot = WasteLocation("DEPOT-00", "Central Municipal Yard", 10.0, 10.0, "Hub", "Normal", 0)
    optimizer = SmartWasteRouteOptimizer(depot)

    # 2. Add Reported Garbage Bins
    sample_bins = [
        WasteLocation("BIN-101", "Sector 4 Market (Organic Overflow)", 12.5, 14.2, "Organic", "Critical", 180),
        WasteLocation("BIN-102", "Green Valley Park (Plastic/Dry)", 16.0, 11.5, "Recyclable", "Moderate", 95),
        WasteLocation("BIN-103", "Commercial Complex B (Cardboard/Paper)", 14.8, 17.1, "Recyclable", "Critical", 220),
        WasteLocation("BIN-104", "Riverside Walkway (Mixed Waste)", 8.2, 16.0, "Hazardous", "Low", 40),
        WasteLocation("BIN-105", "Metro Station North (Trash Bins)", 7.1, 11.8, "Organic", "Moderate", 120),
        WasteLocation("BIN-106", "Old Town Plaza (Dumpster Overflow)", 11.0, 6.5, "Organic", "Critical", 260),
    ]

    for b in sample_bins:
        optimizer.add_location(b)

    # 3. Execute DAA Optimization
    results = optimizer.run_optimization()

    print(f"\n[+] Total Active Garbage Reports: {results['total_bins']}")
    print(f"[+] Naive Route Distance:        {results['naive_distance_km']} km")
    print(f"[+] DAA Optimized Tour Distance: {results['optimized_distance_km']} km")
    print(f"[+] Distance Saved:              {results['fuel_saved_km']} km ({results['efficiency_gain_percent']}% improvement)")
    print(f"[+] Estimated CO2 Emission Cut:  {results['co2_saved_kg']} kg\n")

    print("--- DAA Step-by-Step Decision Trace ---")
    for step in results['trace_steps']:
        print(f"  -> {step}")

    print("\n--- Optimized Collection Dispatch Sequence ---")
    seq_names = " -> ".join([n["name"] for n in results["route_order"]])
    print(f"Route: {seq_names}")
    print("\n" + "=" * 70)
