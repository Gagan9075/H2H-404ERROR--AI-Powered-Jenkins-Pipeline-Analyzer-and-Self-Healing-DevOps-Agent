import streamlit as st
import requests

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
if st.button("Analyze Pipeline"):

    if log_input.strip() == "":
        st.warning("Please enter a log")

    else:
        try:
            response = requests.post(
                API_URL,
                json={"log": log_input}
            )

            data = response.json()
            st.session_state.data = data

        except Exception as e:
            st.error(f"❌ Backend Error: {e}")

# ---------------- DISPLAY ----------------
if st.session_state.data:

    data = st.session_state.data

    ai = data.get("ai_analysis", {})
    fix = data.get("fix", {})
    exec_fix = data.get("exec_fix", {})
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

    fix_text = ai.get("fix", "") or fix.get("fix", "")
    fix_text = fix_text.replace("\\n", "\n").strip()

    steps = [s.strip() for s in fix_text.split("\n") if s.strip()]

    if not steps:
        st.warning("⚠️ No valid steps found")
        st.code(fix_text)
    else:
        for i, step in enumerate(steps, 1):
            st.markdown(f"👉 **Step {i}:** {step}")

    # ---------------- AUTO HEAL ----------------
    st.subheader("⚡ Self-Healing Execution")

    if exec_fix.get("type") == "auto":
        st.success("🤖 Auto-healing available")
        for cmd in exec_fix.get("commands", []):
            st.code(cmd)
    else:
        st.warning(exec_fix.get("message", "Manual fix required"))

    # ---------------- SIMULATION ----------------
    st.subheader("🔁 Pipeline Simulation")

    col1, col2 = st.columns(2)

    with col1:
        st.error("❌ Build Status: FAILED")

    with col2:
        if accuracy > 80:
            st.success("✅ Likely Fixed")
        else:
            st.warning("⚠️ Needs validation")

    # ---------------- ACCURACY ----------------
    st.subheader("📊 Real Accuracy Score")

    st.metric("AI Confidence", f"{accuracy}%")
    st.progress(min(accuracy / 100, 1.0))

    # ---------------- LEARNING DASHBOARD ----------------
    st.subheader("📊 Learning Dashboard")

    try:
        res = requests.get(MEMORY_URL, timeout=10)
        mem_data = res.json()

        failures = mem_data.get("failures", [])

        if not failures:
            st.info("No learning data yet")
        else:
            for f in failures:
                st.write(f"🔹 {f['error']} → {f['count']} times")

    except:
        st.warning("⚠️ Unable to load learning data")