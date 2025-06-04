from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_policy")
def get_policy(user_id: str, app_id: str):
    return {
        "policy": "Policy-Gold" if app_id == "work" else "Policy-Bronze",
        "bandwidth": 80 if app_id == "work" else 30,
        "latency": 20 if app_id == "work" else 100
    }
