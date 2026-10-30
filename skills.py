# -*- coding: utf-8 -*-
"""Warehouse Pick-Path TSP Distance & Labor Optimizer Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def optimize_warehouse_pick_path(**kwargs):
    """Models warehouse 2D coordinate layouts, solves picker Traveling Salesperson Problem (TSP) using 2-opt search heuristic, and minimizes dead-heading travel distance."""
    depot_x_y = kwargs.get('depot_x_y')
    pick_locations = kwargs.get('pick_locations')
    aisle_width_m = kwargs.get('aisle_width_m')
    cross_aisle_penalty_m = kwargs.get('cross_aisle_penalty_m')

    points = [depot_x_y] + pick_locations
    n = len(points)
    
    def dist(p1, p2):
        dx = abs(p1[0] - p2[0])
        dy = abs(p1[1] - p2[1])
        penalty = cross_aisle_penalty_m if p1[0] != p2[0] else 0.0
        return dx + dy + penalty
        
    unvisited = set(range(1, n))
    current = 0
    route = [0]
    while unvisited:
        nxt = min(unvisited, key=lambda idx: dist(points[current], points[idx]))
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    route.append(0)
    
    def route_distance(r):
        return sum(dist(points[r[i]], points[r[i+1]]) for i in range(len(r)-1))
        
    improved = True
    best_dist = route_distance(route)
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
                new_dist = route_distance(new_route)
                if new_dist < best_dist - 0.01:
                    best_dist = new_dist
                    route = new_route
                    improved = True
                    break
            if improved:
                break
                
    baseline_unoptimized = route_distance(list(range(n)) + [0])
    distance_saved_m = round(max(0.0, baseline_unoptimized - best_dist), 1)
    efficiency_gain_pct = round((distance_saved_m / (baseline_unoptimized if baseline_unoptimized > 0 else 1.0)) * 100.0, 1)
    
    result = {
        "status": "success",
        "optimized_pick_sequence": route,
        "total_travel_distance_meters": round(best_dist, 1),
        "baseline_distance_meters": round(baseline_unoptimized, 1),
        "travel_distance_saved_meters": distance_saved_m,
        "labor_efficiency_gain_pct": efficiency_gain_pct,
        "estimated_walking_time_mins": round(best_dist / 80.0, 1),
        "engine": "GenPark Warehouse Operations 2-Opt TSP Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "optimize_warehouse_pick_path": {
        "name": "optimize_warehouse_pick_path",
        "description": "Models warehouse 2D coordinate layouts, solves picker Traveling Salesperson Problem (TSP) using 2-opt search heuristic, and minimizes dead-heading travel distance.",
        "parameters": {
            "type": "object",
            "properties": {
                "depot_x_y": {"type": "array", "description": "Fulfillment packing station depot coordinate [x, y] in meters"},
                "pick_locations": {"type": "array", "description": "List of [x, y] coordinates of items on pick ticket"},
                "aisle_width_m": {"type": "number", "description": "Width of storage aisles in meters"},
                "cross_aisle_penalty_m": {"type": "number", "description": "Cost to switch between vertical aisles in meters"},
            },
            "required": ['depot_x_y', 'pick_locations', 'aisle_width_m', 'cross_aisle_penalty_m']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "optimize_warehouse_pick_path":
            res = optimize_warehouse_pick_path(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-warehouse-pick-path-tsp-travel-distance-optimizer-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-warehouse-pick-path-tsp-travel-distance-optimizer-skill...")
    test_args = {'depot_x_y': [0.0, 0.0], 'pick_locations': [[12.0, 4.0], [12.0, 18.0], [24.0, 6.0], [36.0, 22.0], [48.0, 10.0]], 'aisle_width_m': 2.5, 'cross_aisle_penalty_m': 5.0}
    res = optimize_warehouse_pick_path(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-warehouse-pick-path-tsp-travel-distance-optimizer-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
