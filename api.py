from fastapi import FastAPI
from pydantic import BaseModel
from final_analyzer import (
    ai_analysis_pipeline,
    generate_fix,
    calculate_accuracy,
    update_memory
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
def analyze(request: LogRequest):

    log = request.log

    ai_result = ai_analysis_pipeline(log)

    fix = generate_fix(ai_result)

    accuracy = calculate_accuracy(ai_result)

    update_memory(
        ai_result.get("error_type"),
        ai_result.get("fix")
    )

    return {
        "ai_analysis": ai_result,
        "fix": fix,
        "accuracy": accuracy
    }