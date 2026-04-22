# 🚀 AutoFix CI — Self-Healing DevOps AI

### ⚡ Intelligent, AI-Powered CI/CD Failure Analyzer

> From rule-based debugging → to a **fully AI-driven, self-learning DevOps system**

---

## 📑 Table of Contents

* [🔥 Live System Status](#-live-system-status)
* [🧠 What Makes This Dynamic](#-what-makes-this-dynamic)
* [⚙️ Dynamic Workflow](#️-dynamic-workflow)
* [🌟 Key Capabilities](#-key-capabilities-live-behavior)
* [🏗️ System Architecture](#️-system-architecture-production-ready)
* [📡 API Design](#-api-driven-design)
* [🐳 Dockerized Setup](#-dockerized-setup-one-command-run)
* [📂 Project Structure](#-project-structure-evolving-system)
* [🧪 Dynamic Example](#-dynamic-example)
* [📊 Learning & Accuracy](#-learning--accuracy)
* [🔮 Future Scope](#-future-evolution)
* [🎯 Why This Project Stands Out](#-why-this-project-stands-out)
* [👨‍💻 Team](#-team)
* [📌 Final Thought](#-final-thought)

---

## 🔥 Live System Status

* 🟢 Backend: FastAPI (Microservice)
* 🟢 Frontend: Streamlit (UI Layer)
* 🟢 AI Engine: LLaMA3 via Ollama
* 🟢 Deployment: Dockerized (multi-container)
* 🧠 Memory: Self-learning enabled
* 📊 Accuracy: Dynamically computed

---

## 🧠 What Makes This Dynamic

AutoFix CI is **NOT a static tool**:

* Learns from failures (`memory.json`)
* Uses **AI-first analysis (no fixed patterns)**
* Improves fixes based on success rate
* Works for **unknown/unseen logs**
* Runs as **real microservice architecture**
* Handles failures in real-time pipelines

---

## ⚙️ Dynamic Workflow

```mermaid
flowchart LR
    A[User Log] --> B[Streamlit UI]
    B --> C[FastAPI Backend]
    C --> D[AI Engine (LLaMA3)]
    D --> E[Structured Output]
    E --> F[Fix Generator]
    F --> G[Response to UI]
    G --> H[Memory Update]
```

---

## 🌟 Key Capabilities (Live Behavior)

### 🤖 Fully AI-Driven Analysis

* No dependency on hardcoded patterns
* Understands ANY CI/CD log
* Extracts real root cause

### 🧠 Self-Learning Memory

* Stores past failures
* Tracks success rate
* Improves fixes automatically

### 🛠 Smart Fix Engine

* Generates step-by-step solutions
* Context-aware recommendations

### 📊 Real Accuracy Scoring

* Confidence based on:

  * AI certainty
  * historical success
* Not manually entered

### 🔁 Pipeline Simulation

* Shows:

  * Before fix ❌
  * After fix ✅

### 📊 Learning Dashboard

* Tracks:

  * failure frequency
  * most common issues
  * system learning growth

---

## 🏗️ System Architecture (Production Ready)

```mermaid
flowchart LR
    A[Streamlit UI] --> B[FastAPI Backend]
    B --> C[AI Analyzer]
    C --> D[Ollama (LLaMA3)]
    C --> E[Memory System]
```

---

## 📡 API-Driven Design

### Endpoint

```http
POST /analyze
```

### Request

```json
{
  "log": "your jenkins log here"
}
```

### Response

```json
{
  "ai_analysis": {
    "error_type": "...",
    "root_cause": "...",
    "fix": "..."
  },
  "fix": {
    "issue": "...",
    "fix": "..."
  },
  "accuracy": 90
}
```

---

## 🐳 Dockerized Setup (1-Command Run)

### ✅ Run Full System

```bash
docker-compose up --build
```

---

### 🧠 Pull AI Model (First Time Only)

```bash
docker exec -it ollama ollama pull llama3
```

---

### 🌐 Access

* UI → http://localhost:8501
* API → http://localhost:8000
* AI → http://localhost:11434

---

## 📂 Project Structure (Evolving System)

```
Hack2Hire/
 ├── app.py                  # Streamlit UI
 ├── api.py                  # FastAPI backend
 ├── final_analyzer.py       # AI engine
 ├── docker-compose.yml      # Multi-container setup
 ├── Dockerfile              # Backend container
 ├── Dockerfile.streamlit    # Frontend container
 ├── memory.json             # Learned knowledge
 ├── requirements.txt        # Dependencies
 ├── README.md               # Documentation
```

---

## 🧪 Dynamic Example

### Input

```
ERROR: Repository not found
fatal: Authentication failed
```

### Output

```
Error Type: Git Auth Failure
Root Cause: Invalid credentials or missing access token
Fix:
1. Add Git credentials
2. Use personal access token
3. Update repository URL
```

---

## 📊 Learning & Accuracy

| Feature            | Behavior                    |
| ------------------ | --------------------------- |
| Accuracy           | Dynamic (AI + memory based) |
| Learning           | Automatic                   |
| Adaptability       | High                        |
| Pattern Dependency | ❌ None                      |

---

## 🔮 Future Evolution

* 🔗 Jenkins webhook integration
* 🤖 Auto-fix execution (self-healing pipelines)
* ☁️ Cloud deployment (AWS / Render)
* 📊 Advanced analytics dashboard
* 🔁 Continuous AI improvement loop

---

## 🎯 Why This Project Stands Out

✔ Fully AI-driven (not rule-based)
✔ Microservice architecture
✔ Dockerized production setup
✔ Self-learning system
✔ Real-time DevOps use-case
✔ Handles unknown failures

---

## 👨‍💻 Team

**Team 404 ERROR**

* Gagan M
* Abhisek M

---

## 📌 Final Thought

AutoFix CI is not just a project —
it’s a step toward **autonomous DevOps systems** 🚀

---
