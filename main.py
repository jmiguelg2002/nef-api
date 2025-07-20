from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined policy mappings
policy_rules = {
    "user_001": {
        "work":    {"policy": "Policy-Gold",   "bandwidth": 100.0, "latency": 10.0},
        "gaming":  {"policy": "Policy-Silver", "bandwidth": 50.0,  "latency": 30.0},
        "social":  {"policy": "Policy-Bronze", "bandwidth": 30.0,  "latency": 50.0},
        "messages":{"policy": "Policy-Bronze", "bandwidth": 20.0,  "latency": 70.0}
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
    }
}

@app.get("/get_policy")
def get_policy(user_id: str = Query(...), app_id: str = Query(...)):
    user_policies = policy_rules.get(user_id)
    if user_policies:
        app_policy = user_policies.get(app_id)
        if app_policy:
            return app_policy
    return {"error": "Policy not found"}
