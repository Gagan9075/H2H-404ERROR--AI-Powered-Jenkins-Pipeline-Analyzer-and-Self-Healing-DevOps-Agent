import streamlit as st
import requests
import json
import os
import pandas as pd

# ---------------- CONFIG ----------------
#API_URL = "http://backend:8000/analyze"
#AUTO_HEAL_URL = "https://h2h-404error-ai-powered-jenkins-pipeline-analyz-production.up.railway.app/analyze"
#AUTO_HEAL_URL = "http://backend:8000/auto-heal"

# ---------------- CONFIG ----------------

API_URL = "https://h2h-404error-ai-powered-jenkins-pipeline-analyz-production.up.railway.app/analyze"
MEMORY_URL = "https://h2h-404error-ai-powered-jenkins-pipeline-analyz-production.up.railway.app/memory"

st.set_page_config(page_title="AutoFix CI", layout="wide")

st.title("🚀 AutoFix CI — Self-Healing DevOps AI")
st.markdown("### ⚡ Production-Grade DevOps Failure Analysis")

# ---------------- INPUT ----------------
log_input = st.text_area("📄 Paste Jenkins Log Here", height=200)

# ---------------- SESSION ----------------
if "data" not in st.session_state:
    st.session_state.data = None

# ---------------- ANALYZE ----------------
import requests

if st.button("Analyze Pipeline"):
    if user_input.strip() == "":
        st.warning("Please enter a log")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"log": user_input}
            )

            data = response.json()

            # Extract backend response
            ai = data.get("ai_analysis", {})
            accuracy = data.get("accuracy", 0)

            error_type = ai.get("error_type", "Unknown")
            root_cause = ai.get("root_cause", "Unknown")
            fix_steps = ai.get("fix", "")
            commands = ai.get("commands", [])

            # Display results
            st.subheader("🚨 Incident Summary")
            st.write(f"Error Type: {error_type}")
            st.write(f"AI Confidence: {accuracy}%")
            st.write("Pipeline Status: Failed ❌")

            st.subheader("🧠 Root Cause")
            st.write(root_cause)

            st.subheader("🛠 Fix Plan")
            st.write(fix_steps)

            if commands:
                st.subheader("⚙️ Suggested Commands")
                for cmd in commands:
                    st.code(cmd)

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
# ---------------- DISPLAY ----------------
if st.session_state.data:

    data = st.session_state.data

    ai = data.get("ai_analysis", {})
    fix = data.get("fix", {})
    exec_fix = data.get("exec_fix", {})
    auto_result = data.get("auto_heal_result")
    accuracy = data.get("accuracy", 60)

    # ---------------- SUMMARY ----------------
    st.markdown("## 🚨 Incident Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Error Type", ai.get("error_type", "Unknown"))
    col2.metric("AI Confidence", f"{accuracy}%")
    col3.metric("Pipeline Status", "Failed ❌")

    st.success("🚀 AI detected issue and generated recovery plan")

    # ---------------- AI REASONING ----------------
    st.subheader("🤖 AI Reasoning Engine")

    col1, col2 = st.columns(2)

    with col1:
        st.error(f"🚨 Error Type\n\n{ai.get('error_type')}")

    with col2:
        st.info(f"🧠 Root Cause\n\n{ai.get('root_cause')}")

    # ---------------- FIX ENGINE ----------------
    st.subheader("🛠 Auto Fix Engine")

    st.error(f"🚨 Issue: {fix.get('issue', ai.get('error_type', 'Unknown'))}")

    st.markdown("### 🤖 AI Recommended Fix Plan")

    # ✅ FIX TEXT EXTRACTION
    fix_text = ai.get("fix", "") or fix.get("fix", "")

    # 🔥 CRITICAL FIX: convert escaped newline → real newline
    fix_text = fix_text.replace("\\n", "\n").strip()

    # 🔥 SPLIT STEPS
    steps = [s.strip() for s in fix_text.split("\n") if s.strip()]

    if not steps:
        st.warning("⚠️ No valid steps found. Showing raw output:")
        st.code(fix_text)
    else:
        for i, step in enumerate(steps, 1):
            st.markdown(f"👉 **Step {i}:** {step}")

    # ---------------- AUTO HEAL ----------------
    st.subheader("⚡ Self-Healing Execution")

    # 🔥 AUTO HEAL EXECUTION (AI-BASED)
    auto_heal_result = None

    if exec_fix.get("type") == "auto":
        try:
            response = requests.post(
                AUTO_HEAL_URL,
                json={"commands": exec_fix.get("commands", [])},
                timeout=120
            )
            auto_heal_result = response.json()
        except Exception as e:
            st.error(f"Auto-heal failed: {e}")

    if auto_heal_result:

        steps = auto_heal_result.get("steps", [])
        verify = auto_heal_result.get("verification")

        for step in steps:
            st.code(f"$ {step['command']}")

            if step["status"] == "success":
                st.success(f"✅ {step['output']}")
            else:
                st.error(f"❌ {step['error']}")

        # VERIFY RESULT
        if verify:
            st.markdown("### 🔍 Verification")

            st.code(f"$ {verify.get('command')}")

            if verify.get("status") == "success":
                st.success("✅ System healed successfully!")
            else:
                st.error("❌ Fix failed verification")

    else:
        st.warning(exec_fix.get("message", "No auto-healing available"))

    # ---------------- SIMULATION ----------------
    st.subheader("🔁 Pipeline Simulation")

    col1, col2 = st.columns(2)

    with col1:
        st.error("❌ Build Status: FAILED")

    with col2:
        if auto_heal_result and auto_heal_result.get("verification", {}).get("status") == "success":
            st.success("✅ Build Status: SUCCESS")
        elif accuracy > 80:
            st.success("✅ Likely Fixed")
        else:
            st.warning("⚠️ Fix needs validation")

    # ---------------- ACCURACY ----------------
    st.subheader("📊 Real Accuracy Score")

    st.metric("AI Confidence", f"{accuracy}%")
    st.progress(min(accuracy / 100, 1.0))

    # ---------------- LEARNING DASHBOARD ----------------
    import json
    import os

    st.subheader("📊 Learning Dashboard")

    try:
        res = requests.get(MEMORY_URL, timeout=10)
        data = res.json()

        failures = data.get("failures", [])

        if not failures:
            st.info("No learning data yet")
        else:
            for f in failures:
                st.write(f"🔹 {f['error']} → {f['count']} times")

    except Exception as e:
        st.warning("⚠️ Unable to load learning data")