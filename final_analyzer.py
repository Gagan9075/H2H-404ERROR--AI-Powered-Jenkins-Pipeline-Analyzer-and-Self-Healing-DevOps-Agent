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


# 🔥 UPDATED (self-learning)
def update_memory(error, solution, success=True):
    if not error:
        return

    memory = load_memory()

    for item in memory["failures"]:
        if item["error"] == error:
            item["count"] += 1
            item["success"] = item.get("success", 0) + (1 if success else 0)
            save_memory(memory)
            return

    memory["failures"].append({
        "error": error,
        "solution": solution,
        "count": 1,
        "success": 1 if success else 0
    })

    save_memory(memory)


# 🔥 BEST FIX SELECTION
def get_best_fix(error):
    memory = load_memory()

    best = None
    best_score = 0

    for item in memory["failures"]:
        if item["error"].lower() in error.lower():
            success = item.get("success", 0)
            count = item.get("count", 1)

            score = success / count

            if score > best_score:
                best_score = score
                best = item

    return best


# ---------------- RULE ENGINE ----------------

def rule_based_analysis(log_text):
    log = log_text.lower()

    patterns = [
        ("permission denied", "Permission Denied", "Execution permission missing"),
        ("not found", "Command Not Found", "Missing dependency or wrong path"),
        ("connection refused", "Connection Refused", "Service unavailable"),
        ("exit 1", "Script Failure", "Non-zero exit status"),
        ("no such file", "File Error", "File missing or wrong path"),
        ("authentication failed", "Git/Auth Failure", "Invalid credentials"),
        ("repository not found", "Git/Auth Failure", "Private repo or wrong URL"),
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
You are an expert DevOps failure analyzer.

Analyze ANY Jenkins log.

Return STRICT JSON:

{{
  "error_type": "...",
  "root_cause": "...",
  "fix": "..."
}}

Log:
{log_text}
""",
                "stream": False
            }
        )

        return response.json().get("response", "")

    except Exception as e:
        return str(e)


# ---------------- PARSER ----------------

def parse_ai_response(ai_raw):
    try:
        start = ai_raw.find("{")
        end = ai_raw.rfind("}") + 1

        if start != -1 and end != -1:
            return json.loads(ai_raw[start:end])

    except:
        pass

    return {
        "error_type": "Unknown",
        "root_cause": ai_raw[:200],
        "fix": "Check logs manually"
    }


# ---------------- HYBRID ENGINE ----------------

def hybrid_analysis(log_text):

    rule = rule_based_analysis(log_text)
    memory = check_memory(log_text)

    ai_raw = analyze_with_ai(log_text)
    ai_data = parse_ai_response(ai_raw)

    # 🔥 self-learning override
    best_fix = get_best_fix(ai_data.get("error_type", ""))

    if best_fix:
        ai_data["fix"] = best_fix["solution"]

    return {
        "rule": rule,
        "memory": memory,
        "ai": ai_data
    }


# ---------------- FIX ENGINE ----------------

def generate_fix(ai_data):
    error = (ai_data.get("error_type") or "").lower()
    cause = (ai_data.get("root_cause") or "").lower()

    # ---------------- PERMISSION ----------------
    if "permission" in error:
        return {
            "issue": "Permission Issue",
            "fix": """1. The script does not have execution permission.
2. Grant permission using:
   chmod +x script.sh
3. Re-run the pipeline.
4. If using Jenkins, ensure proper user permissions.

Best Practice:
Always set executable permissions before running scripts.""",
            "fixed_code": "chmod +x script.sh"
        }

    # ---------------- COMMAND NOT FOUND ----------------
    elif "not found" in error:
        return {
            "issue": "Command Not Found",
            "fix": """1. The required command/tool is missing.
2. Install the dependency:
   sudo apt install <tool-name>
3. Verify installation:
   <tool-name> --version
4. Check if PATH is configured correctly.

Best Practice:
Use dependency checks before pipeline execution.""",
            "fixed_code": "sudo apt install <tool>"
        }

    # ---------------- CONNECTION ----------------
    elif "connection" in error:
        return {
            "issue": "Network / Service Issue",
            "fix": """1. The system failed to connect to a service.
2. Check if the service is running:
   systemctl status <service>
3. Test connectivity:
   ping localhost
4. Verify firewall/network rules.

Best Practice:
Always ensure services are running before pipeline execution.""",
            "fixed_code": "ping localhost"
        }

    # ---------------- FILE ERROR ----------------
    elif "file" in error:
        return {
            "issue": "File Path Issue",
            "fix": """1. The required file is missing or path is incorrect.
2. Verify file existence:
   ls -l /path/to/file
3. Update correct file path in script.
4. Ensure file permissions are correct.

Best Practice:
Always validate file paths in pipeline scripts.""",
            "fixed_code": "ls -l /path/to/file"
        }

    # ---------------- GIT AUTH ----------------
    elif "git" in error or "auth" in error:
        return {
            "issue": "Git Authentication Failure",
            "fix": """1. Authentication failed while accessing repository.
2. Use personal access token instead of password.
3. Update clone command:
   git clone https://<token>@github.com/repo.git
4. Verify repository access permissions.

Best Practice:
Use secure credential storage (Jenkins credentials manager).""",
            "fixed_code": "git clone https://<token>@github.com/repo.git"
        }

    # ---------------- DEFAULT ----------------
    return {
        "issue": ai_data.get("error_type"),
        "fix": f"""1. {ai_data.get("root_cause")}
2. Suggested Fix:
   {ai_data.get("fix")}
3. Review logs for more details.

Best Practice:
Add proper error handling and logging in pipeline.""",
        "fixed_code": ""
    }


# ---------------- REAL ACCURACY ----------------

def evaluate_accuracy(rule, ai_data, memory):

    score = 0

    rule_error = (rule or {}).get("error", "").lower()
    ai_error = (ai_data.get("error_type") or "").lower()
    mem_error = (memory or {}).get("error", "").lower()

    if rule_error and rule_error in ai_error:
        score += 40

    if mem_error and mem_error in ai_error:
        score += 30

    if ai_error != "unknown":
        score += 20

    if score == 0:
        score = 50

    return min(score, 100)


# ---------------- AUTONOMOUS EVAL ----------------

def autonomous_evaluation(logs_list):
    results = []
    error_groups = defaultdict(list)

    for log in logs_list:

        result = hybrid_analysis(log)

        ai = result["ai"]

        results.append({
            "log": log,
            "error_type": ai.get("error_type"),
        })

        error_groups[ai.get("error_type")].append(log)

    return {
        "results": results,
        "unique_errors": len(error_groups)
    }