# 🤖 AutoFix CI: AI-Powered Jenkins Failure Analyzer & Self-Healing Agent

> 🚧 Currently under development as part of Hack2Hire 1.0

---

## 🚀 About the Project

In real-world software development, CI/CD pipelines often fail due to small issues like missing dependencies, failing tests, or configuration mistakes. Debugging these failures usually takes a lot of time because the logs are long and difficult to understand.

This project aims to make that process easier.

AutoFix CI is a system that reads Jenkins pipeline logs, understands what went wrong, and explains it in simple language. It can also suggest possible fixes and even retry certain failures automatically.

---

## 🎯 What I’m Trying to Solve

* Developers spend too much time reading confusing logs
* Many failures are repetitive but still require manual debugging
* There is no simple way to understand errors quickly

This project tries to reduce that effort by making failure analysis smarter and faster.

---

## 🧠 What the System Does

* Reads Jenkins pipeline logs
* Identifies the type of error (dependency issue, test failure, timeout, etc.)
* Converts technical errors into simple explanations
* Suggests possible fixes
* Retries builds in case of temporary failures

---

## 🌟 What Makes This Different

Instead of just analyzing errors once, this system tries to learn over time.

* It keeps track of past failures and remembers what worked before
* If the same issue happens again, it can suggest a solution faster
* It also provides a confidence level for its explanations

The goal is to make the system not just reactive, but gradually smarter.

---

## 🛠️ Tech Stack

* Jenkins (to run pipelines)
* Docker (to easily set up Jenkins)
* Python (for log analysis and automation)
* OpenAI / Ollama (for generating explanations)
* Streamlit (optional, for displaying results)

---

## ⚙️ How It Works (Simple Flow)

1. A Jenkins pipeline runs
2. If it fails, the logs are collected
3. The system analyzes the logs using rules and AI
4. It explains the issue in simple terms
5. It suggests or performs a fix
6. The result is stored for future reference

---

## 📈 Expected Outcome

The goal is to make debugging faster and easier, especially for repetitive issues. Instead of spending time reading logs, developers can directly understand what went wrong and how to fix it.

---

## 🔮 Future Improvements

* Automatically creating issue tickets (like Jira)
* Predicting failures before they happen
* Supporting other CI/CD tools
* Better UI for monitoring

---

## 👨‍💻 Team

**Team Name:** 404 ERROR  

**Members:**
- Gagan M  
- Abhishek M  

Built as part of Hack2Hire 1.0
