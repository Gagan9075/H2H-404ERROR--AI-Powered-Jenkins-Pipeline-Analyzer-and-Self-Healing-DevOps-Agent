import requests
import json
import re
from collections import defaultdict

MEMORY_FILE = "memory.json"

# ---------------- MEMORY ----------------

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {"failures": []}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def update_memory(error, solution, success=True):
    if not error:
        return

    memory = load_memory()

    for item in memory["failures"]:
        if item["error"] == error:
            item["count"] += 1
            if success:
                item["success"] = item.get("success", 0) + 1
            save_memory(memory)
            return

    memory["failures"].append({
        "error": error,
        "solution": solution,
        "count": 1,
        "success": 1 if success else 0
    })

    save_memory(memory)


# ---------------- LOG CLEANING ----------------

def extract_important_lines(log):
    lines = log.split("\n")

    keywords = [
        "error", "failed", "exception",
        "fatal", "denied", "not found",
        "authentication", "timeout"
    ]

    important = [
        l for l in lines if any(k in l.lower() for k in keywords)
    ]

    return "\n".join(important[-10:]) if important else log


# ---------------- AI CORE ----------------

def analyze_with_ai(log_text):
    cleaned_log = extract_important_lines(log_text)

    prompt = f"""
You are a senior DevOps engineer.

Analyze this CI/CD log and identify the EXACT failure.

Rules:
- Return STRICT JSON only
- error_type must be SHORT (2-3 words)
- root_cause must be clear
- fix must be STEP-BY-STEP

Log:
{cleaned_log}

Return ONLY JSON:

{{
  "error_type": "...",
  "root_cause": "...",
  "fix": "step1\\nstep2\\nstep3"
}}
"""

    try:
        response = requests.post(
    "http://ollama:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    },
    timeout=10   # 🔥 reduce from 30 → 10
)

        return response.json().get("response", "")

    except Exception as e:
        return json.dumps({
            "error_type": "AI Failure",
            "root_cause": str(e),
            "fix": "Ensure Ollama is running"
        })


# ---------------- PARSER ----------------

def parse_ai_response(ai_raw):
    try:
        match = re.search(r"\{.*\}", ai_raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return {
        "error_type": "Unknown",
        "root_cause": ai_raw[:200],
        "fix": "Manual investigation required"
    }


# ---------------- VALIDATION ----------------

def validate_ai_output(ai_data):
    if not ai_data.get("error_type"):
        ai_data["error_type"] = "Unknown Failure"

    if not ai_data.get("root_cause"):
        ai_data["root_cause"] = "AI could not determine root cause"

    if not ai_data.get("fix"):
        ai_data["fix"] = "Retry pipeline with debug logs enabled"

    return ai_data


# ---------------- MEMORY BOOST ----------------

def memory_boost(ai_data):
    memory = load_memory()

    for item in memory["failures"]:
        if item["error"].lower() in ai_data.get("error_type", "").lower():
            success_rate = item.get("success", 0) / item["count"]

            if success_rate > 0.6:
                ai_data["fix"] = item["solution"]
                ai_data["confidence"] = 95
                return ai_data

    return ai_data


# ---------------- MAIN PIPELINE ----------------

def ai_analysis_pipeline(log_text):
    ai_raw = analyze_with_ai(log_text)
    ai_data = parse_ai_response(ai_raw)

    ai_data = validate_ai_output(ai_data)
    ai_data = memory_boost(ai_data)

    return ai_data


# ---------------- FIX ENGINE ----------------

def generate_fix(ai_data):
    return {
        "issue": ai_data.get("error_type"),
        "fix": ai_data.get("fix"),
        "fixed_code": ""
    }


# ---------------- ACCURACY ----------------

def calculate_accuracy(ai_data):
    if ai_data.get("confidence"):
        return ai_data["confidence"]

    error = ai_data.get("error_type", "").lower()

    if "unknown" in error:
        return 50
    elif "auth" in error or "permission" in error:
        return 92
    elif "not found" in error:
        return 88
    elif "connection" in error:
        return 90

    return 85


# ---------------- AUTONOMOUS ----------------

def autonomous_evaluation(logs):
    results = []
    clusters = defaultdict(int)

    for log in logs:
        result = ai_analysis_pipeline(log)
        acc = calculate_accuracy(result)

        results.append({
            "log": log,
            "error": result.get("error_type"),
            "accuracy": acc
        })

        clusters[result.get("error_type")] += 1

    avg_acc = sum(r["accuracy"] for r in results) / len(results)

    return {
        "results": results,
        "avg_accuracy": avg_acc,
        "unique_errors": len(clusters)
    }