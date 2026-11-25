# 🌱 Volunteer AI: Student Growth Assistant

> **Empowering educators to understand every student's unique voice through Multimodal AI.**

![Project Status](https://img.shields.io/badge/Status-Prototype-blue) ![Python](https://img.shields.io/badge/Python-3.10%2B-green) ![FastAPI](https://img.shields.io/badge/Framework-FastAPI-teal) ![License](https://img.shields.io/badge/License-MIT-orange)

## 📖 Introduction

**Volunteer AI** is a web-based application designed to support volunteer teachers in under-resourced areas. It explores how AI can help teachers reflect on students' interests and learning needs beyond traditional academic grading.

The current prototype uses **teacher observation notes and GLM-4** to draft a **Growth Analysis Report**, covering:
* 🧘 **Potential Profile**: Personality and hidden talents.
* 🚀 **Learning Advice**: Actionable, psychological-based guidance.
* 📊 **Competency Radar**: AI-scored metrics on Innovation, Empathy, Drive, etc.

Image and audio uploads are accepted, but `analyze_image_for_context()` and `analyze_audio_to_text()` in [`agent_core.py`](agent_core.py) currently return `None`. GLM-4V image analysis and audio transcription are planned. Generated profiles and scores are suggestions for educator review, not validated psychological assessments.

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI
* **AI Engine**: ZhipuAI GLM-4 (text reports); GLM-4V integration planned
* **Frontend**: HTML5, Jinja2 Templates, Tailwind CSS
* **Visualization**: Chart.js (Radar Charts)
* **Local Server**: Uvicorn / FastAPI (`main:app`)

## ✨ Key Features

1.  **Observation-Based Reports**: Generates a report from teacher notes; image and audio analysis remain TODOs.
2.  **Learning Suggestions**: Drafts reflections on student interests and support needs for teacher review.
3.  **Visualized Reports**: Professional radar charts and Markdown-rendered advice.
4.  **English Interface**: Current templates and the report-generation prompt use English; full bilingual localization is not implemented.

## 🚀 Local Setup

Use Python **3.10+** and run from the repository root so template and upload paths resolve correctly.

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file (already ignored by Git) containing your ZhipuAI key:

```dotenv
ZHIPU_API_KEY=your_zhipu_api_key
```

Then start the FastAPI app:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. A key is required at startup, and submitting the form calls the GLM-4 API. For a local trial, use fictional student notes and sample media: the form currently requires both photo and audio files even though their analysis is not implemented. Uploads are stored under `uploads/` and served at `/uploads`; only the latest report is kept in app memory. This is a local prototype, not a multi-user deployment setup.

---
*Created with ❤️ for the future of education.*
