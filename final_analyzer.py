import requests
import json
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


def check_memory(log_text):
    memory = load_memory()

    for item in memory["failures"]:
        if item["error"].lower() in log_text.lower():
            return item

    return None


def update_memory(error, solution):
    if not error:
        return

    memory = load_memory()

    for item in memory["failures"]:
        if item["error"] == error:
            item["count"] += 1
            save_memory(memory)
            return

    memory["failures"].append({
        "error": error,
        "solution": solution,
        "count": 1
    })

    save_memory(memory)


# ---------------- NORMALIZER (NEW 🔥) ----------------

def normalize_log(log_text):
    return log_text.lower().strip()


# ---------------- RULE ENGINE ----------------

def rule_based_analysis(log_text):
    log = normalize_log(log_text)

    patterns = [
        ("permission denied", "Permission Denied", "Execution permission missing"),
        ("not found", "Command Not Found", "Missing dependency or wrong path"),
        ("connection refused", "Connection Refused", "Service unavailable"),
        ("exit 1", "Script Failure", "Non-zero exit status"),
        ("no such file", "File Error", "File missing or wrong path")
    ]

    for keyword, error, reason in patterns:
        if keyword in log:
            return {"error": error, "reason": reason}

    return None


# ---------------- AI ----------------

def analyze_with_ai(log_text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
You are a senior DevOps engineer.

Analyze the Jenkins log carefully and extract the exact failure.

Log:
{log_text}

Return STRICT JSON ONLY:

{{
  "error_type": "short label",
  "root_cause": "exact reason",
  "fix": "practical solution"
}}
""",
                "stream": False
            }
        )

        return response.json().get("response", "")

    except Exception as e:
        return json.dumps({
            "error_type": "AI Error",
            "root_cause": str(e),
            "fix": "Check AI service"
        })


# ---------------- PARSER (IMPROVED 🔥) ----------------

def parse_ai_response(ai_raw):
    try:
        start = ai_raw.find("{")
        end = ai_raw.rfind("}") + 1

        if start != -1 and end != -1:
            return json.loads(ai_raw[start:end])

    except Exception:
        pass

    return {
        "error_type": "Unknown",
        "root_cause": ai_raw[:200],
        "fix": "Manual investigation required"
    }


# ---------------- HYBRID ANALYSIS (NEW 🔥) ----------------

def hybrid_analysis(log_text):
    """
    Rule-first → AI fallback
    """

    rule = rule_based_analysis(log_text)

    if rule:
        return {
            "error_type": rule["error"],
            "root_cause": rule["reason"],
            "fix": "Apply rule-based fix"
        }

    ai_raw = analyze_with_ai(log_text)
    return parse_ai_response(ai_raw)


# ---------------- FIX ENGINE ----------------

def generate_fix(ai_data):
    error = (ai_data.get("error_type") or "").lower()
    cause = (ai_data.get("root_cause") or "").lower()

    if "permission" in error:
        return {
            "issue": "Permission Issue",
            "fix": "Run chmod +x on script",
            "fixed_code": "chmod +x script.sh"
        }

    elif "not found" in error:
        return {
            "issue": "Command Missing",
            "fix": "Install dependency or fix PATH",
            "fixed_code": "sudo apt install <tool>"
        }

    elif "connection" in error:
        return {
            "issue": "Network Issue",
            "fix": "Check service/network",
            "fixed_code": "ping localhost"
        }

    elif "file" in error:
        return {
            "issue": "File Path Issue",
            "fix": "Verify file exists",
            "fixed_code": "ls -l"
        }

    elif "exit" in cause:
        return {
            "issue": "Script Failure",
            "fix": "Remove exit 1",
            "fixed_code": "echo Success"
        }

    return {
        "issue": ai_data.get("error_type"),
        "fix": ai_data.get("fix"),
        "fixed_code": ""
    }


def generate_advanced_fix(ai_data):
    return {
        "primary_fix": ai_data.get("fix"),
        "alternative_fix": "Retry with debug logs",
        "best_practice": "Use proper error handling",
        "example_code": "set -e"
    }


# ---------------- CONFIDENCE ----------------

def confidence_score(ai_data):
    error = ai_data.get("error_type", "").lower()

    if error == "unknown":
        return 60

    weights = {
        "permission": 95,
        "connection": 90,
        "file": 88,
        "script": 92,
        "command": 89
    }

    for key, value in weights.items():
        if key in error:
            return value

    return 85


# ---------------- AUTONOMOUS EVALUATION ----------------

def autonomous_evaluation(logs_list):
    results = []
    error_groups = defaultdict(list)

    for log in logs_list:

        result = hybrid_analysis(log)

        error_type = result.get("error_type", "Unknown")
        confidence = confidence_score(result)

        results.append({
            "log": log,
            "error_type": error_type,
            "confidence": confidence
        })

        error_groups[error_type].append(log)

    total = len(results)
    unique_errors = len(error_groups)

    avg_conf = sum(r["confidence"] for r in results) / total

    consistency = sum(len(v)**2 for v in error_groups.values()) / (total**2)

    return {
        "results": results,
        "unique_errors": unique_errors,
        "avg_confidence": avg_conf,
        "consistency": round(consistency * 100, 2)
    }