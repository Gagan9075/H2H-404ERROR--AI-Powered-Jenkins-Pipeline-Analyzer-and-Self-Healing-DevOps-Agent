from fastapi import FastAPI
from pydantic import BaseModel
from final_analyzer import *

app = FastAPI()


# ---------------- REQUEST MODEL ----------------
class LogRequest(BaseModel):
    log: str


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {
        "message": "🚀 AutoFix CI API Running",
        "status": "healthy"
    }


# ---------------- ANALYZE ----------------
@app.post("/analyze")
def analyze(request: LogRequest):

    log = request.log

    # 🔥 FULL HYBRID RESULT
    result = hybrid_analysis(log)

    rule = result["rule"]
    memory = result["memory"]
    ai = result["ai"]

    # 🔧 FIX
    fix = generate_fix(ai)

    # 📊 REAL ACCURACY
    accuracy = evaluate_accuracy(rule, ai, memory)

    # 🧠 SELF LEARNING
    update_memory(ai.get("error_type"), ai.get("fix"))

    return {
        "rule_based": rule,
        "memory": memory,
        "ai_analysis": ai,
        "fix": fix,
        "accuracy": accuracy
    }