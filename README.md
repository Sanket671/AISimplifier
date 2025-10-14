# ⚖️ Legal Document Simplifier AI

> 🧠 Transform complex legal jargon into simple, human-understandable summaries powered by **Google Gemini 2.5 Pro**.

---

## 🌐 Live Demo

🖥️ **Frontend (Netlify)**: [https://aisimplifierfrontend.netlify.app](https://aisimplifierfrontend.netlify.app)  
⚙️ **Backend (Render)**: [https://aisimplifier.onrender.com](https://aisimplifier.onrender.com)

---

## 🧩 Overview

**Legal Document Simplifier AI** is a full-stack web application that helps users simplify lengthy legal documents into clear, digestible summaries.  
Users can upload `.txt` files or paste raw legal text, and the AI (Gemini 2.5 Pro) processes it to return a structured, plain-language summary.

This project bridges **AI**, **Flask**, and **web deployment**, demonstrating a real-world **AI SaaS pipeline**.

---

## ✨ Key Features

- 📂 Upload or paste text directly into the web interface  
- ⚙️ **AI-powered simplification** via Google Gemini 2.5 Pro  
- 🔁 **Automatic API key rotation** — seamlessly switches keys when a limit is hit  
- 🧠 Thematic “few-shot prompting” for context-aware summaries  
- 🚀 Deployed with:
  - Frontend on **Netlify**
  - Backend on **Render**
- 💬 Health-check route for backend monitoring  
- 🔐 Secure CORS configuration between client & server

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Python 3.10+, Flask |
| **AI Model** | Google Gemini 2.5 Pro |
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Hosting** | Render (API) + Netlify (UI) |
| **Dependencies** | `google-generativeai`, `python-dotenv`, `flask-cors` |

---

## 📂 Project Structure

```plaintext
legal-document-simplifier/
├── backend/
│   ├── app.py               # Flask app with /simplify and /health routes
│   ├── config.py            # Environment variable & key config
│   ├── debug_gemini.py      # Gemini connection test script
│   ├── requirements.txt     # Python dependencies
│   ├── utils/
│   │   └── ai_simplifier.py # Gemini API client + key rotation logic
│   └── .env.example         # Template for environment keys
│
├── frontend/
│   ├── index.html           # Main interface
│   ├── script.js            # Fetch logic for AI simplification
│   ├── style.css            # Page styling
│   └── public/              # Static assets
│
├── sample_data/
│   └── legal_docs/
│       ├── sample_1.txt
│       ├── sample_2.txt
│       └── sample_3.txt
│
├── run.py                   # Optional script to run both servers locally
├── render.yaml              # Backend Render deployment config
└── README.md                # You are here!
```

---

## ⚙️ Setup & Local Run

### 1. Clone the repository

```bash
git clone https://github.com/Sanket671/AISimplifier.git
cd AISimplifier
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Add Gemini API keys

Create a `.env` file in the `backend/` folder:

```env
GEMINI_API_KEY_1="your_first_key"
GEMINI_API_KEY_2="your_second_key"
# add more if needed
```

### 4. Run backend

```bash
python app.py
```

Backend will start on `http://127.0.0.1:5001` (the project uses PORT=5001 in `.env`).

### 5. Run frontend

```bash
cd ../frontend
python -m http.server 3000
```

Then visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧠 How It Works (AI Pipeline)

1. User uploads or pastes text → JS sends it to Flask API
2. Flask routes the request to `AISimplifier.simplify_text()`
3. The class constructs a rich *few-shot prompt* to guide Gemini
4. Gemini 2.5 Pro returns a simplified, section-wise summary
5. The frontend displays the result beautifully formatted

This design ensures **coherent**, **context-aware**, and **accurate**
simplification even for long, dense documents.

---

## ☁️ Deployment Summary

| Component    | Platform | Config                                        |
| ------------ | -------- | --------------------------------------------- |
| **Backend**  | Render   | `render.yaml`, `Procfile`, `requirements.txt` |
| **Frontend** | Netlify  | Deployed via GitHub (`/frontend`)             |

CORS, environment variables, and production builds are properly configured for seamless communication between both services.

---

## 🧠 Cloud Computing Concepts Implemented

This project demonstrates a number of core cloud computing concepts across deployment, storage, AI services, and security. Below is a concise summary you can use in a presentation or viva.

### 1. Cloud Deployment (PaaS – Platform as a Service)

Concept: Hosting the backend on a managed cloud platform that handles servers, scaling, and runtime.

Where used:
- Flask backend is deployed on **Render**, which is a PaaS.

How to explain:
> “We deployed our Flask backend on Render, a cloud PaaS, which automatically handles deployment, uptime, and scaling without manual server setup.”

---

### 2. Frontend Hosting via Cloud CDN (Static Web Hosting)

Concept: Cloud-hosted static frontend with global delivery for fast performance.

Where used:
- Frontend hosted on **Netlify**, which uses a global CDN.

How to explain:
> “Our frontend runs on Netlify, which uses a global content delivery network to serve users quickly across regions.”

---

### 3. Cloud Database – Database as a Service (DBaaS)

Concept: Using a fully managed database hosted on the cloud.

Where used:
- **MongoDB Atlas** stores simplified document records, user data, and logs.

How to explain:
> “We used MongoDB Atlas, a cloud-hosted NoSQL database service, to securely store data and make it accessible from anywhere.”

---

### 4. Cloud Storage Service – Cloudinary Integration

Concept: Using third-party cloud storage for media or files.

Where used:
- **Cloudinary** stores uploaded legal documents or images securely and provides managed URLs.

How to explain:
> “We integrated Cloudinary for storing and managing files on the cloud instead of local storage — a real example of cloud storage as a service.”

---

### 5. AI as a Cloud Service (AIaaS)

Concept: Using AI models hosted on the cloud via APIs.

Where used:
- **Google Gemini 2.5 Pro API** simplifies legal text through cloud-based AI processing.

How to explain:
> “We used Google Gemini through its API — the AI processing happens on Google’s cloud servers, representing AI-as-a-Service.”

---

### 6. Secure Environment Management (.env)

Concept: Cloud security via environment variables and secret keys.

Where used:
- All credentials — Gemini API keys, MongoDB URI, and Cloudinary secrets — are stored in `.env` and loaded using `python-dotenv`.

How to explain:
> “We securely manage sensitive credentials through environment variables, which is a standard cloud security practice.”

---

### 7. Fault Tolerance and Auto Key Rotation (Reliability Concept)

Concept: Ensuring uninterrupted operation using redundancy and fallback mechanisms.

Where used:
- The `ai_simplifier.py` class rotates among multiple Gemini API keys when rate-limited.

How to explain:
> “We implemented a fault-tolerant design that automatically switches Gemini API keys if one exceeds its quota — improving cloud reliability.”

---

### 8. API Communication Across Clouds (Distributed Architecture)

Concept: Different cloud services interacting through secure APIs.

Where used:
- **Frontend (Netlify)** → **Backend (Render)** → **MongoDB Atlas / Cloudinary / Gemini AI**.

How to explain:
> “Our app uses a distributed, multi-cloud architecture — frontend, backend, and services are on different clouds but communicate through secure REST APIs.”

---

### 9. Auto Scaling and Monitoring (Render Features)

Concept: Automatic adjustment of resources and service reliability.

Where used:
- Render auto-scales the Flask server, restarts it on failure, and provides logs.

How to explain:
> “Render provides built-in monitoring and auto-scaling, so our backend remains available and adjusts to user load automatically.”

---

### 10. Logging and Observability

Concept: Tracking system activity for debugging and performance monitoring.

Where used:
- Errors and API failures are logged (see backend logs) with timestamps for observability.

How to explain:
> “We implemented logging for API errors and operations, similar to cloud monitoring tools that track performance.”

---

### 11. CORS and Secure Cloud Communication

Concept: Controlling access between different cloud origins securely.

Where used:
- Flask backend uses **Flask-CORS** to allow only trusted frontend origins.

How to explain:
> “Since our frontend and backend are on different cloud domains, we configured CORS policies for secure cross-origin communication.”

---

### 12. Continuous Integration / Continuous Deployment (CI/CD)

Concept: Automatic building and deployment directly from version control.

Where used:
- Both **Render** and **Netlify** connect to GitHub for automatic deployments on pushes.

How to explain:
> “We used CI/CD pipelines — every GitHub commit triggers an automatic build and redeployment on Render and Netlify.”

---

## 🎤 Short Summary (for viva or presentation)

> “Our project implements real cloud computing — the backend runs on Render (PaaS), frontend on Netlify (CDN), database on MongoDB Atlas (DBaaS), and file storage on Cloudinary. We also integrated Google Gemini AI as AIaaS, used environment variables for security, and achieved multi-cloud communication through REST APIs. This setup demonstrates deployment, storage, AI integration, and scalability — all key cloud computing concepts.”

---

## 🧾 Example Output

**Input:** 5-page sale deed legal document
**Output:**

> Simplified explanation of property registration, sale deed clauses, seller & buyer rights, and document requirements — all in easy language and structured sections.

---

## 🧰 Debugging

To test Gemini connectivity or diagnose key issues:

```bash
cd backend
python debug_gemini.py
```

You’ll get detailed logs confirming which API key is active and whether Gemini is reachable.

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and build upon it.

---

## 💬 Author

👤 **Sanket Motewar**
🎓 B.Tech (VIT Pune)
💡 Passionate about building AI-driven, real-world engineering solutions.

> “From a local folder to two live servers talking through AI — this project represents real end-to-end deployment power.”

---

## ⭐ Acknowledgements

* Google Gemini API for NLP capabilities
* Render & Netlify for free-tier hosting
* ChatGPT (AI Pair Programmer 😄) for deployment debugging and optimization support
