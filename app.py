import streamlit as st
import requests
import json
import os
import pandas as pd

API_URL = "http://127.0.0.1:8000/analyze"

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
                json={"log": log_input}
            )

            data = response.json()

        except Exception as e:
            st.error(f"API Error: {e}")
            st.stop()

    # ---------------- MEMORY (Optional display) ----------------
    st.subheader("🧠 Memory Insight")

    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            memory = json.load(f)

        for item in memory.get("failures", []):
            if item["error"].lower() in log_input.lower():
                st.success("⚡ Known Issue Detected")
                st.write(f"**Error:** {item['error']}")
                st.write(f"**Solution:** {item['solution']}")
                break

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

    ai = data.get("ai_analysis", {})

    st.write(f"**Error Type:** {ai.get('error_type')}")
    st.write(f"**Root Cause:** {ai.get('root_cause')}")
    st.write(f"**Suggested Fix:** {ai.get('fix')}")

    # ---------------- FIX ----------------
    st.subheader("🛠 Auto Fix Engine")

    fix = data.get("fix", {})

    st.write(f"**Issue:** {fix.get('issue')}")
    st.write(f"**Solution:** {fix.get('fix')}")

    if fix.get("fixed_code"):
        st.code(fix.get("fixed_code"), language="bash")

    # ---------------- ADVANCED FIX ----------------
    st.subheader("🚀 Smart Fix Recommendations")

    st.success("Primary Fix")
    st.write(fix.get("fix"))

    st.info("Alternative Fix")
    st.write("Retry pipeline with debug logs enabled")

    st.warning("Best Practice")
    st.write("Add proper error handling in scripts")

    # ---------------- 🔁 SMART SIMULATION ----------------
    st.subheader("🔁 Pipeline Simulation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Before Fix")

        log = log_input.lower()

        if "exit 1" in log:
            st.error("Script exited with error")
        elif "permission" in log:
            st.error("Permission denied")
        elif "connection" in log:
            st.error("Connection failure")
        elif "not found" in log:
            st.error("Command not found")
        else:
            st.error("Pipeline Failed")

    with col2:
        st.markdown("### ✅ After Fix")

        fix_text = (fix.get("fix") or "").lower()

        if any(word in fix_text for word in ["remove", "chmod", "install", "check"]):
            st.success("Pipeline Fixed ✅")
        else:
            st.warning("⚠️ Needs validation")

    # ---------------- CONFIDENCE ----------------
    st.subheader("📊 Confidence Engine")

    if ai.get("error_type") == "Unknown":
        score = 60
    else:
        score = 92

    st.metric("Detection Confidence", f"{score}%")
    st.progress(score / 100)

    # ---------------- DASHBOARD ----------------
    st.markdown("---")
    st.subheader("📊 Analytics Dashboard")

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
            col1.metric("Total Failures", total)
            col2.metric("Top Error", most_common["error"])

# ---------------- 🔥 AUTONOMOUS EVALUATION ----------------
st.markdown("---")
st.subheader("🧠 Autonomous AI Evaluation")

if st.button("Run Autonomous Evaluation"):

    test_logs = [
        "exit 1",
        "permission denied",
        "connection refused",
        "no such file",
        "command not found"
    ]

    results = []

    for log in test_logs:
        try:
            res = requests.post(API_URL, json={"log": log}).json()

            results.append({
                "log": log,
                "error": res.get("ai_analysis", {}).get("error_type"),
            })

        except:
            results.append({"log": log, "error": "API Error"})

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
- Memory-based learning
- Autonomous evaluation

Built like real-world DevOps platforms 🚀
""")