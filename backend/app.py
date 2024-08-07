from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware
# Import your solve_routing_problem function from another file
from last_mile import solve_routing_problem
import json 

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Order(BaseModel):
    names: List[str]
    locations: List[Tuple[float, float]]
    demands: List[int]
    capacities: List[int]
    vehicles: int

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/solve-routing-problem")
async def solve_routing_problem_endpoint(orders: Order):
    if orders is None:
        raise HTTPException(status_code=400, detail="Missing 'order' query parameter")
    # Process the request with the provided 'order' parameter
    # return {"message": f"Received order: {orders}"}
    coordinates = orders.locations
    demands = orders.demands
    vehicle_capacities = orders.capacities
    num_vehicles = orders.vehicles
    
    results = solve_routing_problem(coordinates, demands, vehicle_capacities, num_vehicles)
    if results is not None:
        data = []
        for i, result in enumerate(results):
            data.append({
                'driver': i,
                'route': result['route'],
                'total_distance': result['total_distance'],
                'parcels_delivered': result['parcels_delivered']
            })
        
        return data
    else:
        raise HTTPException(status_code=404, detail="No Solution")
