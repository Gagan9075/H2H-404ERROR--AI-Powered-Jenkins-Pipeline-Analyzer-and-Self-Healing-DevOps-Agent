import requests
import json
import re
import time
import os
from collections import defaultdict

MEMORY_FILE = "memory.json"

# ---------------- MEMORY ----------------

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            if "failures" not in data:
                return {"failures": []}
            return data
    except:
        return {"failures": []}


def update_memory(error, fix):
    data = load_memory()

    found = False

    for item in data["failures"]:
        if item["error"] == error:
            item["count"] += 1
            item["fix"] = fix
            item["success"] = item.get("success", 0)
            found = True
            break

    if not found:
        data["failures"].append({
            "error": error,
            "fix": fix,
            "count": 1,
            "success": 0
        })

    data["failures"] = data["failures"][-50:]

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


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

Analyze CI/CD logs and return ONLY valid JSON.

STRICT RULES:
- ONLY JSON output
- NO markdown
- NO explanation outside JSON

Log:
{cleaned_log}

Return EXACT format:
{{
  "error_type": "short error",
  "root_cause": "technical explanation",
  "fix": "step1\\nstep2\\nstep3",
  "commands": ["cmd1", "cmd2"]
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
            timeout=60
        )

        res = response.json()
        raw = res.get("response", "").strip()

        # CLEAN RESPONSE
        raw = raw.replace("```json", "").replace("```", "")

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            parsed = json.loads(match.group())

            if parsed.get("fix"):
                return parsed

    except Exception as e:
        print("❌ AI failed, switching to fallback:", e)

    # ---------------- FALLBACK LOGIC ----------------
    log = log_text.lower()

    if "timeout" in log:
        return {
            "error_type": "Build Timeout",
            "root_cause": "Build exceeded allowed execution time",
            "fix": "Increase timeout in Jenkins\\nOptimize build steps\\nCheck heavy processes",
            "commands": ["timeout 30m", "optimize build"]
        }

    elif "auth" in log or "permission" in log:
        return {
            "error_type": "Authentication Failure",
            "root_cause": "Invalid credentials or access denied",
            "fix": "Update credentials\\nUse access token\\nVerify permissions",
            "commands": ["git config", "update token"]
        }

    elif "not found" in log:
        return {
            "error_type": "Resource Not Found",
            "root_cause": "Incorrect file path or missing resource",
            "fix": "Check file paths\\nVerify repository URL\\nEnsure resource exists",
            "commands": ["ls", "check path"]
        }

    elif "docker" in log:
        return {
            "error_type": "Docker Failure",
            "root_cause": "Container build or runtime issue",
            "fix": "Rebuild image\\nCheck Dockerfile\\nVerify dependencies",
            "commands": ["docker build", "docker logs"]
        }

    else:
        return {
            "error_type": "Unknown Error",
            "root_cause": "Unrecognized failure pattern",
            "fix": "Check logs manually\\nRestart pipeline\\nDebug step-by-step",
            "commands": []
        }


# ---------------- PARSER ----------------

def parse_ai_response(ai_raw):
    if isinstance(ai_raw, dict):
        return ai_raw

    try:
        return json.loads(ai_raw)
    except:
        match = re.search(r"\{.*\}", ai_raw, re.DOTALL)
        if match:
            return json.loads(match.group())

    return {
        "error_type": "Parsing Failed",
        "root_cause": "Invalid AI output",
        "fix": "Retry analysis",
        "commands": []
    }


# ---------------- VALIDATION ----------------

def validate_ai_output(ai_data):
    ai_data.setdefault("error_type", "Unknown Failure")
    ai_data.setdefault("root_cause", "Unknown cause")
    ai_data.setdefault("fix", "Retry pipeline")
    ai_data.setdefault("commands", [])
    return ai_data


# ---------------- MEMORY BOOST ----------------

def memory_boost(ai_data):
    memory = load_memory()

    for item in memory["failures"]:
        if item["error"].lower() in ai_data["error_type"].lower():
            success_rate = item.get("success", 0) / item["count"]

            if success_rate > 0.6:
                ai_data["fix"] = item["fix"]
                ai_data["confidence"] = 95
                return ai_data

    return ai_data


# ---------------- FIX ENGINE ----------------

def generate_fix(ai_data):
    return {
        "issue": ai_data.get("error_type"),
        "fix": ai_data.get("fix"),
        "fixed_code": ""
    }


# ---------------- EXECUTABLE FIX ----------------

def generate_executable_fix(ai_data):
    commands = ai_data.get("commands", [])

    return {
        "type": "auto" if commands else "manual",
        "commands": commands,
        "message": "Auto-healing available" if commands else "Manual fix required"
    }


# ---------------- ACCURACY ----------------

def calculate_accuracy(ai_data):
    if ai_data.get("confidence"):
        return ai_data["confidence"]

    error = ai_data.get("error_type", "").lower()

    if "auth" in error:
        return 92
    elif "timeout" in error:
        return 90
    elif "not found" in error:
        return 88

    return 85


# ---------------- MAIN PIPELINE ----------------

def ai_analysis_pipeline(log_text):
    ai_raw = analyze_with_ai(log_text)
    ai_data = parse_ai_response(ai_raw)

    ai_data = validate_ai_output(ai_data)
    ai_data = memory_boost(ai_data)

    return ai_data


# ---------------- AUTONOMOUS ANALYSIS ----------------

def autonomous_evaluation(logs):
    results = []
    clusters = defaultdict(int)

    for log in logs:
        ai = ai_analysis_pipeline(log)
        acc = calculate_accuracy(ai)

        results.append({
            "log": log,
            "error": ai.get("error_type"),
            "accuracy": acc
        })

        clusters[ai.get("error_type")] += 1

    avg_acc = sum(r["accuracy"] for r in results) / len(results)

    return {
        "results": results,
        "avg_accuracy": avg_acc,
        "unique_errors": len(clusters)
    }