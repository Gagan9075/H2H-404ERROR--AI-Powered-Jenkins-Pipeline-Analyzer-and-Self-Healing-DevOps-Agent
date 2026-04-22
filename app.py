import streamlit as st
import requests
import json
import os
import pandas as pd

API_URL = "http://backend:8000/analyze"

st.set_page_config(page_title="AutoFix CI", layout="wide")

st.title("🚀 AutoFix CI — Self-Healing DevOps AI")
st.markdown("### ⚡ Production-Grade DevOps Failure Analysis")

log_input = st.text_area("📄 Paste Jenkins Log Here", height=200)

if st.button("🔍 Analyze Pipeline"):

    if not log_input.strip():
        st.warning("Please enter a Jenkins log!")
        st.stop()

    try:
        response = requests.post(API_URL, json={"log": log_input}, timeout=20)
        data = response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        st.stop()

    ai = data.get("ai_analysis", {})
    fix = data.get("fix", {})
    accuracy = data.get("accuracy", 60)

    # ---------------- AI ----------------
    st.subheader("🤖 AI Reasoning Engine")

    st.write(f"**Error Type:** {ai.get('error_type')}")
    st.write(f"**Root Cause:** {ai.get('root_cause')}")
    st.write(f"**Suggested Fix:** {ai.get('fix')}")

    # ---------------- EXPLANATION ----------------
    st.markdown("### 📘 Explanation")
    st.info(ai.get("root_cause"))

    # ---------------- FIX ----------------
    st.subheader("🛠 Auto Fix Engine")

    st.error(f"🚨 {fix.get('issue')}")

    st.markdown("### 🛠 Step-by-Step Fix Guide")
    st.code(fix.get("fix"))

    # ---------------- SIMULATION ----------------
    st.subheader("🔁 Pipeline Simulation")

    col1, col2 = st.columns(2)

    with col1:
        st.error("Pipeline Failed ❌")

    with col2:
        if accuracy > 70:
            st.success("Pipeline Fixed ✅")
        else:
            st.warning("Needs validation ⚠️")

    # ---------------- ACCURACY ----------------
    st.subheader("📊 Real Accuracy Score")

    st.metric("AI Accuracy", f"{accuracy}%")
    st.progress(accuracy / 100)

    # ---------------- MEMORY DASHBOARD ----------------
    st.markdown("---")
    st.subheader("📊 Learning Dashboard")

    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            mem = json.load(f)

        failures = mem.get("failures", [])

        if failures:
            df = pd.DataFrame(failures)

            st.bar_chart(df.set_index("error")["count"])

            total = sum([f["count"] for f in failures])
            most_common = max(failures, key=lambda x: x["count"])

            col1, col2 = st.columns(2)
            col1.metric("Total Learned", total)
            col2.metric("Top Error", most_common["error"])