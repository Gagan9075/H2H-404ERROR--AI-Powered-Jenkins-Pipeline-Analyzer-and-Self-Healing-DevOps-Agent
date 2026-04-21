import streamlit as st
import requests
import json
import os
import pandas as pd

from final_analyzer import hybrid_analysis, generate_fix

# 🔥 Use this for local run
#  API_URL = "http://localhost:8000/analyze"

# 🔥 Use this for Docker
API_URL = "http://backend:8000/analyze"

st.set_page_config(page_title="AutoFix CI", layout="wide")

# ---------------- HEADER ----------------
st.title("🚀 AutoFix CI — Self-Healing DevOps AI")
st.markdown("### ⚡ Production-Grade DevOps Failure Analysis")

# ---------------- INPUT ----------------
log_input = st.text_area("📄 Paste Jenkins Log Here", height=200)

# ---------------- ANALYSIS ----------------
if st.button("🔍 Analyze Pipeline"):

    if not log_input.strip():
        st.warning("Please enter a Jenkins log!")
        st.stop()

    # ---------------- API CALL ----------------
    with st.spinner("Calling FastAPI backend..."):
        try:
            response = requests.post(
                API_URL,
                json={"log": log_input},
                timeout=10
            )

            if response.status_code != 200:
                raise Exception("API failed")

            data = response.json()

        except Exception as e:
            st.error(f"⚠️ API Error: {e}")
            st.warning("Switching to local AI fallback...")

            # 🔥 fallback if API fails
            ai_result = hybrid_analysis(log_input)
            fix = generate_fix(ai_result)

            data = {
                "rule_based": None,
                "memory": None,
                "ai_analysis": ai_result,
                "fix": fix,
                "accuracy": 50
            }

    # ---------------- MEMORY ----------------
    st.subheader("🧠 Memory Insight")

    memory = data.get("memory")

    if memory:
        st.success("⚡ Known Issue Detected")
        st.write(f"**Error:** {memory.get('error')}")
        st.write(f"**Solution:** {memory.get('solution')}")
    else:
        st.info("No matching memory pattern")

    # ---------------- RULE ----------------
    st.subheader("⚙️ Rule-Based Engine")

    rule = data.get("rule_based")

    if rule:
        col1, col2 = st.columns(2)
        col1.error(rule.get("error"))
        col2.info(rule.get("reason"))
    else:
        st.info("No rule-based pattern detected")

    # ---------------- AI ----------------
    st.subheader("🤖 AI Reasoning Engine")

    ai = data.get("ai_analysis") or {
        "error_type": "Unknown",
        "root_cause": "Not detected",
        "fix": "Manual investigation required"
    }

    st.write(f"**Error Type:** {ai.get('error_type')}")
    st.write(f"**Root Cause:** {ai.get('root_cause')}")
    st.write(f"**Suggested Fix:** {ai.get('fix')}")

    st.markdown("### 📘 Explanation")
    st.info(ai.get("root_cause"))

# ---------------- FIX ----------------
st.subheader("🛠 Auto Fix Engine")

fix = data.get("fix", {})

st.write(f"### 🚨 Issue Detected")
st.error(fix.get("issue"))

# 🔥 NEW: Explanation section
st.markdown("### 📘 Root Cause Explanation")
st.info(ai.get("root_cause"))

# 🔥 NEW: Detailed fix guide
st.markdown("### 🛠 Step-by-Step Fix Guide")
st.markdown(f"```\n{fix.get('fix')}\n```")

# 🔥 Show command separately (clean UX)
if fix.get("fixed_code"):
    st.markdown("### 💻 Suggested Command")
    st.code(fix.get("fixed_code"), language="bash")

    # ---------------- ADVANCED FIX ----------------
    st.subheader("🚀 Smart Fix Recommendations")

    st.success("Primary Fix")
    st.write(fix.get("fix"))

    st.info("Alternative Fix")
    st.write("Retry pipeline with debug logs enabled")

    st.warning("Best Practice")
    st.write("Add proper error handling in scripts")

    # ---------------- PIPELINE SIMULATION ----------------
    st.subheader("🔁 Pipeline Simulation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Before Fix")

        error_type = (ai.get("error_type") or "").lower()

        if "permission" in error_type:
            st.error("Permission denied")
        elif "connection" in error_type:
            st.error("Connection failure")
        elif "not found" in error_type:
            st.error("Command not found")
        elif "git" in error_type or "auth" in error_type:
            st.error("Git authentication failed")
        elif "file" in error_type:
            st.error("File missing or incorrect path")
        else:
            st.error("Pipeline Failed")

    with col2:
        st.markdown("### ✅ After Fix")

        accuracy = data.get("accuracy", 50)

        if accuracy > 70:
            st.success("Pipeline Fixed ✅")
        else:
            st.warning("⚠️ Needs validation")

    # ---------------- REAL ACCURACY ----------------
    st.subheader("📊 Real Accuracy Score")

    accuracy = data.get("accuracy", 50)

    st.metric("AI Accuracy", f"{accuracy}%")
    st.progress(accuracy / 100)

    # ---------------- DASHBOARD ----------------
    st.markdown("---")
    st.subheader("📊 Learning Dashboard")

    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            data_mem = json.load(f)

        failures = data_mem.get("failures", [])

        if failures:
            df = pd.DataFrame(failures)

            st.bar_chart(df.set_index("error")["count"])

            total = sum([f["count"] for f in failures])
            most_common = max(failures, key=lambda x: x["count"])

            col1, col2 = st.columns(2)
            col1.metric("Total Failures Learned", total)
            col2.metric("Most Frequent Error", most_common["error"])

        else:
            st.info("No learning data yet")

# ---------------- AUTONOMOUS EVALUATION ----------------
st.markdown("---")
st.subheader("🧠 Autonomous AI Evaluation")

if st.button("Run Autonomous Evaluation"):

    test_logs = [
        "exit 1",
        "permission denied",
        "connection refused",
        "no such file",
        "authentication failed",
        "repository not found"
    ]

    results = []

    for log in test_logs:
        try:
            res = requests.post(API_URL, json={"log": log}).json()

            results.append({
                "log": log,
                "error": res.get("ai_analysis", {}).get("error_type"),
                "accuracy": res.get("accuracy", 0)
            })

        except:
            results.append({
                "log": log,
                "error": "API Error",
                "accuracy": 0
            })

    df = pd.DataFrame(results)

    st.dataframe(df)
    st.bar_chart(df["error"].value_counts())

    st.success("AI evaluated across multiple logs 🚀")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 System Overview")
st.sidebar.write("""
AutoFix CI is an enterprise DevOps AI system:

- FastAPI backend (microservice)
- Streamlit frontend (UI layer)
- Hybrid AI + Rule engine
- Self-learning memory
- Real accuracy scoring
- Autonomous evaluation

Designed for modern CI/CD pipelines 🚀
""")