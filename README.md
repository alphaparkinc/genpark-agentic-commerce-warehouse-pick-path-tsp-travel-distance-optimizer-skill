# Warehouse Pick-Path TSP Distance & Labor Optimizer Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `optimize_warehouse_pick_path`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Models warehouse 2D coordinate layouts, solves picker Traveling Salesperson Problem (TSP) using 2-opt search heuristic, and minimizes dead-heading travel distance.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Fulfillment & Warehousing)`

## MCP Tool Specification
### `optimize_warehouse_pick_path`
Parameters:
- `depot_x_y` (list): Fulfillment packing station depot coordinate [x, y] in meters
- `pick_locations` (list): List of [x, y] coordinates of items on pick ticket
- `aisle_width_m` (float): Width of storage aisles in meters
- `cross_aisle_penalty_m` (float): Cost to switch between vertical aisles in meters

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-warehouse-pick-path-tsp-travel-distance-optimizer-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-warehouse-pick-path-tsp-travel-distance-optimizer-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
