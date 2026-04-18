import streamlit as st
import json
from final_analyzer import (
    rule_based_analysis,
    analyze_with_ai,
    generate_fix,
    confidence_score,
    check_memory,
    update_memory
)

st.set_page_config(page_title="AutoFix CI", layout="wide")

# ---------------- HEADER ----------------
st.title("🚀 AutoFix CI — Self-Healing DevOps AI")
st.markdown("### ⚡ From Failure Detection → Automated Fix Generation")

# ---------------- INPUT ----------------
log_input = st.text_area("📄 Paste Jenkins Log Here", height=200)

# ---------------- ANALYSIS ----------------
if st.button("🔍 Analyze Pipeline"):

    if not log_input.strip():
        st.warning("Please enter a Jenkins log!")
        st.stop()

    # ---------------- MEMORY ----------------
    st.subheader("🧠 Memory Intelligence")
    memory = check_memory(log_input)

    if memory:
        st.success("⚡ Known Issue Detected")

        col1, col2 = st.columns(2)
        col1.write(f"**Error:** {memory['error']}")
        col2.write(f"**Solution:** {memory['solution']}")

        st.metric("Memory Confidence", "100%")
        st.info("Validating using full analysis...")

    # ---------------- RULE ----------------
    st.subheader("⚙️ Rule-Based Engine")
    rule = rule_based_analysis(log_input)

    if rule:
        col1, col2 = st.columns(2)
        col1.error(rule["error"])
        col2.info(rule["reason"])
    else:
        st.info("No rule-based issue detected")

    # ---------------- AI ----------------
    st.subheader("🤖 AI Reasoning Engine")

    with st.spinner("Running LLaMA3 analysis..."):
        ai_raw = analyze_with_ai(log_input)

    # Try to parse JSON (important upgrade 🔥)
    try:
        ai_data = json.loads(ai_raw)

        st.success("AI Structured Output")

        st.write(f"**Error Type:** {ai_data.get('error_type')}")
        st.write(f"**Root Cause:** {ai_data.get('root_cause')}")
        st.write(f"**Fix:** {ai_data.get('fix')}")

    except:
        st.warning("AI returned unstructured output")
        st.code(ai_raw)

    # ---------------- FIX ----------------
    st.subheader("🛠 Auto-Fix Engine")

    fix = generate_fix(log_input)

    st.write(f"**Issue:** {fix['issue']}")
    st.write(f"**Solution:** {fix['fix']}")

    if fix["fixed_code"]:
        st.code(fix["fixed_code"], language="bash")

    # ---------------- SIMULATION (🔥 UNIQUE FEATURE) ----------------
    st.subheader("🔁 Pipeline Simulation")

    original = "echo Hello Jenkins\nexit 1"
    fixed = fix["fixed_code"] if fix["fixed_code"] else original

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Before Fix")
        st.code(original, language="bash")
        st.error("Status: FAILED")

    with col2:
        st.markdown("### ✅ After Fix")
        st.code(fixed, language="bash")

        if "exit 1" not in fixed:
            st.success("Status: SUCCESS")
        else:
            st.warning("Still failing")

    # ---------------- CONFIDENCE ----------------
    st.subheader("📊 Confidence Engine")

    score = confidence_score(log_input)

    st.metric("Detection Confidence", f"{score}%")
    st.progress(score / 100)

    # ---------------- STORE ----------------
    update_memory(fix["issue"], fix["fix"])
    st.success("System learned from this failure ✅")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 System Overview")
st.sidebar.write("""
AutoFix CI is an intelligent DevOps assistant:

- Hybrid Analysis (Rule + AI)
- Self-Healing Fix Engine
- Memory-Based Learning
- Pipeline Simulation

Designed for modern CI/CD systems 🚀
""")