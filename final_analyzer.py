import requests
import json

MEMORY_FILE = "memory.json"


# ---------------- MEMORY SYSTEM ----------------

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def check_memory(log_text):
    memory = load_memory()
    for key in memory:
        if key in log_text:
            return memory[key]
    return None


def store_memory(log_text, solution):
    memory = load_memory()
    memory[log_text[:50]] = solution
    save_memory(memory)


# ---------------- RULE-BASED ANALYZER ----------------

def rule_based_analysis(log_text):
    log_text = log_text.lower()

    if "cannot run program" in log_text:
        return "Environment Error: Wrong OS command used"

    elif "exit 1" in log_text:
        return "Script Failure: Script exited with error"

    elif "marked build as failure" in log_text:
        return "Build Failure detected"

    return None


# ---------------- AI ANALYZER ----------------

def analyze_with_ai(log_text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
You are an expert DevOps engineer.

Analyze the Jenkins log below VERY CAREFULLY.

Log:
{log_text}

Give output in this format:

Error Type:
Reason (exact root cause from log):
Fix (specific solution):
""",
                "stream": False
            }
        )

        data = response.json()

        print("\nDEBUG RESPONSE:", data)  # 👈 helps debug

        return data.get("response", "No AI response received")

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------------- MAIN SYSTEM ----------------

def main():
    with open("logs.txt", "r") as f:
        logs = f.read()

    print("\n--- Checking Memory ---")
    memory_result = check_memory(logs)

    if memory_result:
        print("Found in memory ✅")
        print(memory_result)
        return

    print("\n--- Rule-based Analysis ---")
    rule_result = rule_based_analysis(logs)

    if rule_result:
        print(rule_result)

    print("\n--- AI Analysis ---")
    ai_result = analyze_with_ai(logs)
    print(ai_result)

    print("\n--- Storing in Memory ---")
    store_memory(logs, ai_result)
    print("Stored for future use ✅")


if __name__ == "__main__":
    main()