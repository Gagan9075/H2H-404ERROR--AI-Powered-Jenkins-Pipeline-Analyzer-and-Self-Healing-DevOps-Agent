import requests
import json
import re

MEMORY_FILE = "memory.json"

# ---------------- LOG PREPROCESSING (NEW 🔥) ----------------

def clean_log(log_text):
    """Remove noise and keep important lines"""
    lines = log_text.split("\n")
    important = []

    for line in lines:
        if any(keyword in line.lower() for keyword in [
            "error", "fail", "exception", "exit", "cannot"
        ]):
            important.append(line)

    return "\n".join(important) if important else log_text


def extract_error_keyword(log_text):
    """Extract main error keyword for memory matching"""
    patterns = ["exit 1", "cannot run program", "failure", "exception"]

    for p in patterns:
        if p in log_text.lower():
            return p

    return "unknown"


# ---------------- MEMORY SYSTEM ----------------

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
    keyword = extract_error_keyword(log_text)

    for item in memory["failures"]:
        if item["error"] == keyword:
            return item

    return None


def update_memory(error, solution):
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


# ---------------- RULE-BASED ANALYZER ----------------

def rule_based_analysis(log_text):
    log = log_text.lower()

    if "cannot run program" in log:
        return {
            "error": "Environment Error",
            "reason": "Wrong OS command (Windows vs Linux)"
        }

    elif "exit 1" in log:
        return {
            "error": "Script Failure",
            "reason": "Script exited with non-zero status"
        }

    elif "marked build as failure" in log:
        return {
            "error": "Build Failure",
            "reason": "Pipeline step failed"
        }

    return None


# ---------------- FIX GENERATOR ----------------

def generate_fix(log_text):
    log = log_text.lower()

    if "exit 1" in log:
        return {
            "issue": "exit 1",
            "fix": "Remove 'exit 1' or handle errors properly",
            "fixed_code": "echo Build Successful"
        }

    elif "cannot run program" in log:
        return {
            "issue": "cannot run program",
            "fix": "Use Linux-compatible commands",
            "fixed_code": "echo Hello from Linux"
        }

    return {
        "issue": "unknown",
        "fix": "Manual investigation required",
        "fixed_code": ""
    }


# ---------------- CONFIDENCE ENGINE ----------------

def confidence_score(log_text):
    log = log_text.lower()

    if "exit 1" in log:
        return 95
    elif "cannot run program" in log:
        return 90
    elif "failure" in log:
        return 85

    return 60


# ---------------- SEVERITY ENGINE (NEW 🔥) ----------------

def detect_severity(log_text):
    log = log_text.lower()

    if "exit 1" in log or "failure" in log:
        return "HIGH"
    elif "warning" in log:
        return "MEDIUM"
    return "LOW"


# ---------------- AI ANALYZER (IMPROVED 🔥) ----------------

def analyze_with_ai(log_text):
    try:
        cleaned = clean_log(log_text)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
You are a senior DevOps engineer.

Analyze this Jenkins log:

{cleaned}

Return ONLY JSON:

{{
  "error_type": "...",
  "root_cause": "...",
  "fix": "..."
}}
""",
                "stream": False
            }
        )

        data = response.json()
        result = data.get("response", "")

        # Try parsing JSON safely
        try:
            parsed = json.loads(result)
            return json.dumps(parsed, indent=2)
        except:
            return result  # fallback

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- MAIN SYSTEM ----------------

def main():
    with open("logs.txt", "r") as f:
        logs = f.read()

    print("\n🚀 AutoFix CI - Analysis Started")

    # CLEAN LOG
    logs = clean_log(logs)

    # MEMORY
    print("\n--- Memory Check ---")
    memory = check_memory(logs)

    if memory:
        print("⚡ Known Issue Found")
        print(memory)
        return

    # RULE
    print("\n--- Rule-based Analysis ---")
    rule = rule_based_analysis(logs)

    if rule:
        print(f"Error: {rule['error']}")
        print(f"Reason: {rule['reason']}")

    # AI
    print("\n--- AI Analysis ---")
    ai = analyze_with_ai(logs)
    print(ai)

    # FIX
    print("\n--- Auto Fix ---")
    fix = generate_fix(logs)
    print(fix)

    # SEVERITY
    print("\n--- Severity ---")
    print(detect_severity(logs))

    # CONFIDENCE
    print("\n--- Confidence ---")
    print(f"{confidence_score(logs)}%")

    # STORE
    update_memory(fix["issue"], fix["fix"])
    print("\n✅ Memory Updated")


if __name__ == "__main__":
    main()

import requests
import json
import re

MEMORY_FILE = "memory.json"

# ---------------- LOG PREPROCESSING (NEW 🔥) ----------------

def clean_log(log_text):
    """Remove noise and keep important lines"""
    lines = log_text.split("\n")
    important = []

    for line in lines:
        if any(keyword in line.lower() for keyword in [
            "error", "fail", "exception", "exit", "cannot"
        ]):
            important.append(line)

    return "\n".join(important) if important else log_text


def extract_error_keyword(log_text):
    """Extract main error keyword for memory matching"""
    patterns = ["exit 1", "cannot run program", "failure", "exception"]

    for p in patterns:
        if p in log_text.lower():
            return p

    return "unknown"


# ---------------- MEMORY SYSTEM ----------------

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
    keyword = extract_error_keyword(log_text)

    for item in memory["failures"]:
        if item["error"] == keyword:
            return item

    return None


def update_memory(error, solution):
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


# ---------------- RULE-BASED ANALYZER ----------------

def rule_based_analysis(log_text):
    log = log_text.lower()

    if "cannot run program" in log:
        return {
            "error": "Environment Error",
            "reason": "Wrong OS command (Windows vs Linux)"
        }

    elif "exit 1" in log:
        return {
            "error": "Script Failure",
            "reason": "Script exited with non-zero status"
        }

    elif "marked build as failure" in log:
        return {
            "error": "Build Failure",
            "reason": "Pipeline step failed"
        }

    return None


# ---------------- FIX GENERATOR ----------------

def generate_fix(log_text):
    log = log_text.lower()

    if "exit 1" in log:
        return {
            "issue": "exit 1",
            "fix": "Remove 'exit 1' or handle errors properly",
            "fixed_code": "echo Build Successful"
        }

    elif "cannot run program" in log:
        return {
            "issue": "cannot run program",
            "fix": "Use Linux-compatible commands",
            "fixed_code": "echo Hello from Linux"
        }

    return {
        "issue": "unknown",
        "fix": "Manual investigation required",
        "fixed_code": ""
    }


# ---------------- CONFIDENCE ENGINE ----------------

def confidence_score(log_text):
    log = log_text.lower()

    if "exit 1" in log:
        return 95
    elif "cannot run program" in log:
        return 90
    elif "failure" in log:
        return 85

    return 60


# ---------------- SEVERITY ENGINE (NEW 🔥) ----------------

def detect_severity(log_text):
    log = log_text.lower()

    if "exit 1" in log or "failure" in log:
        return "HIGH"
    elif "warning" in log:
        return "MEDIUM"
    return "LOW"


# ---------------- AI ANALYZER (IMPROVED 🔥) ----------------

def analyze_with_ai(log_text):
    try:
        cleaned = clean_log(log_text)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
You are a senior DevOps engineer.

Analyze this Jenkins log:

{cleaned}

Return ONLY JSON:

{{
  "error_type": "...",
  "root_cause": "...",
  "fix": "..."
}}
""",
                "stream": False
            }
        )

        data = response.json()
        result = data.get("response", "")

        # Try parsing JSON safely
        try:
            parsed = json.loads(result)
            return json.dumps(parsed, indent=2)
        except:
            return result  # fallback

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- MAIN SYSTEM ----------------

def main():
    with open("logs.txt", "r") as f:
        logs = f.read()

    print("\n🚀 AutoFix CI - Analysis Started")

    # CLEAN LOG
    logs = clean_log(logs)

    # MEMORY
    print("\n--- Memory Check ---")
    memory = check_memory(logs)

    if memory:
        print("⚡ Known Issue Found")
        print(memory)
        return

    # RULE
    print("\n--- Rule-based Analysis ---")
    rule = rule_based_analysis(logs)

    if rule:
        print(f"Error: {rule['error']}")
        print(f"Reason: {rule['reason']}")

    # AI
    print("\n--- AI Analysis ---")
    ai = analyze_with_ai(logs)
    print(ai)

    # FIX
    print("\n--- Auto Fix ---")
    fix = generate_fix(logs)
    print(fix)

    # SEVERITY
    print("\n--- Severity ---")
    print(detect_severity(logs))

    # CONFIDENCE
    print("\n--- Confidence ---")
    print(f"{confidence_score(logs)}%")

    # STORE
    update_memory(fix["issue"], fix["fix"])
    print("\n✅ Memory Updated")


if __name__ == "__main__":
    main()