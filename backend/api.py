from fastapi import FastAPI
from pydantic import BaseModel

from executor import execute_commands
from final_analyzer import (
    ai_analysis_pipeline,
    generate_fix,
    calculate_accuracy,
    update_memory,
    generate_executable_fix
)

app = FastAPI()


class LogRequest(BaseModel):
    log: str


class FixRequest(BaseModel):
    commands: list


@app.get("/")
def home():
    return {"message": "🚀 AutoFix CI API Running"}


@app.post("/analyze")
def analyze(request: LogRequest):
    try:
        log = request.log

        ai_result = ai_analysis_pipeline(log)
        fix = generate_fix(ai_result)
        exec_fix = generate_executable_fix(ai_result)
        accuracy = calculate_accuracy(ai_result)

        update_memory(ai_result.get("error_type"), ai_result.get("fix"))

        result = {
            "ai_analysis": ai_result,
            "fix": fix,
            "exec_fix": exec_fix,
            "accuracy": accuracy
        }

        print("FINAL RESPONSE:", result)

        return result

    except Exception as e:
        print("❌ ERROR:", str(e))

        return {
            "ai_analysis": {
                "error_type": "System Error",
                "root_cause": str(e),
                "fix": "Backend failure"
            },
            "fix": {},
            "exec_fix": {},
            "accuracy": 0
        }


@app.post("/auto-heal")
def auto_heal(request: FixRequest):
    try:
        results = execute_commands(request.commands)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/memory")
def get_memory():
    import json
    import os

    if not os.path.exists("memory.json"):
        return {"failures": []}

    with open("memory.json", "r") as f:
        return json.load(f)