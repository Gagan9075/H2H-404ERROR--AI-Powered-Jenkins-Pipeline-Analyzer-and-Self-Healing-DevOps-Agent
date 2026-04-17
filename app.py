import streamlit as st
import subprocess

st.title("🚀 AutoFix CI - AI DevOps Failure Analyzer")

st.write("Upload your Jenkins log file and analyze failures using AI")

uploaded_file = st.file_uploader("Upload logs.txt")

if uploaded_file:
    log_text = uploaded_file.read().decode("utf-8")

    # Save logs
    with open("logs.txt", "w") as f:
        f.write(log_text)

    st.success("Log uploaded successfully!")

    if st.button("Analyze"):
        st.text("Running analysis...")

        result = subprocess.run(
            ["python", "final_analyzer.py"],
            capture_output=True,
            text=True
        )

        st.text_area("Analysis Result", result.stdout, height=400)