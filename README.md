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

Backend will start on `http://127.0.0.1:5000`.

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
