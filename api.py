from fastapi import FastAPI
from pydantic import BaseModel

from final_analyzer import (
    rule_based_analysis,
    analyze_with_ai,
    parse_ai_response,
    generate_fix
)

app = FastAPI()


class LogRequest(BaseModel):
    log: str


@app.get("/")
def home():
    return {
        "message": "🚀 AutoFix CI API Running",
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(data: LogRequest):

    log = data.log

    # Rule-based
    rule = rule_based_analysis(log)

    # AI
    ai_raw = analyze_with_ai(log)
    ai_data = parse_ai_response(ai_raw)

    # Fallback if AI fails
    if ai_data.get("error_type") == "Unknown" and rule:
        ai_data = {
            "error_type": rule["error"],
            "root_cause": rule["reason"],
            "fix": "Fix based on rule-based detection"
        }

    # Fix generation
    fix = generate_fix(ai_data)

    return {
        "rule": rule,
        "ai": ai_data,
        "fix": fix
    }