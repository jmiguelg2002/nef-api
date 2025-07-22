from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Allow CORS from any origin (for browser & Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Policy rule store (in-memory)
policy_rules = {
    "user_001": {
        "work": {"policy": "Policy-Gold", "bandwidth": 100.0, "latency": 10.0},
        "gaming": {"policy": "Policy-Silver", "bandwidth": 50.0, "latency": 30.0},
        "social": {"policy": "Policy-Bronze", "bandwidth": 30.0, "latency": 50.0},
        "messages": {"policy": "Policy-Bronze", "bandwidth": 20.0, "latency": 70.0}
    },
    "user_002": {
        "work":    {"policy": "Policy-Gold",   "bandwidth": 80.0,  "latency": 12.0},
        "gaming":  {"policy": "Policy-Gold",   "bandwidth": 70.0,  "latency": 20.0},
        "social":  {"policy": "Policy-Silver", "bandwidth": 40.0,  "latency": 40.0},
        "messages":{"policy": "Policy-Bronze", "bandwidth": 25.0,  "latency": 65.0}
    },
    "user_003": {
        "work":    {"policy": "Policy-Silver", "bandwidth": 70.0,  "latency": 18.0},
        "gaming":  {"policy": "Policy-Gold",   "bandwidth": 90.0,  "latency": 15.0},
        "social":  {"policy": "Policy-Silver", "bandwidth": 35.0,  "latency": 45.0},
        "messages":{"policy": "Policy-Bronze", "bandwidth": 25.0,  "latency": 60.0}
    },
    "user_004": {
        "work":    {"policy": "Policy-Gold",   "bandwidth": 95.0,  "latency": 11.0},
        "gaming":  {"policy": "Policy-Silver", "bandwidth": 60.0,  "latency": 28.0},
        "social":  {"policy": "Policy-Bronze", "bandwidth": 30.0,  "latency": 55.0},
        "messages":{"policy": "Policy-Bronze", "bandwidth": 20.0,  "latency": 70.0}
    },
    "user_abc": {
        "work":    {"policy": "Policy-Silver", "bandwidth": 60.0,  "latency": 15.0},
        "gaming":  {"policy": "Policy-Bronze", "bandwidth": 30.0,  "latency": 35.0},
        "social":  {"policy": "Policy-Bronze", "bandwidth": 25.0,  "latency": 60.0},
        "messages":{"policy": "Policy-Bronze", "bandwidth": 20.0,  "latency": 70.0}
    },
    # Add others here as needed...
}

# POST body model
class PolicyRequest(BaseModel):
    user_id: str
    app_id: str
    policy: str
    bandwidth: float
    latency: float

@app.get("/get_policy")
def get_policy(user_id: str = Query(...), app_id: str = Query(...)):
    """Query policy for a given user/app"""
    user_policies = policy_rules.get(user_id)
    if user_policies:
        app_policy = user_policies.get(app_id)
        if app_policy:
            return app_policy
    return {"error": "Policy not found"}

@app.post("/provision_policy")
def provision_policy(policy_data: PolicyRequest):
    """Provision new or update existing policy for a user/app"""
    if policy_data.user_id not in policy_rules:
        policy_rules[policy_data.user_id] = {}

    policy_rules[policy_data.user_id][policy_data.app_id] = {
        "policy": policy_data.policy,
        "bandwidth": policy_data.bandwidth,
        "latency": policy_data.latency
    }
    return {"status": "Policy provisioned", "data": policy_rules[policy_data.user_id][policy_data.app_id]}
