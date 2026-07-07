<div align="center">
  
# 🏛️ CivicAI

**A Generative AI-powered digital platform empowering citizens to easily access government services, report public issues, and understand civic schemes.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-blue?style=flat)](https://deepmind.google/technologies/gemini/)

</div>

---

## 2. Overview

Navigating government infrastructure is often an overwhelming experience. Citizens struggle to understand complex eligibility criteria for welfare schemes, face language barriers when accessing digital services, and lack transparent, easy-to-use platforms to report civic issues like damaged roads or power outages.

**CivicAI** leverages the power of Generative AI to bridge this gap. By acting as an intelligent Digital Government Assistant, it simplifies bureaucratic jargon, matches users to relevant schemes based on their profile, and automatically categorizes public complaints for efficient routing.

**Objectives:**
- Democratize access to civic information.
- Provide a seamless, natural language interface for reporting issues.
- Eliminate confusion around document requirements and eligibility.
- Create a lightweight, high-performance, and modular architecture.

---

## 3. Features

### 🤖 AI Chat Assistant
- **Purpose:** A conversational agent that answers civic queries in plain language.
- **Workflow:** Users ask questions about government services, and the AI retrieves accurate answers based on the verified `schemes.json` context.
- **AI Prompt Flow:** Employs a strict system persona (`GOVERNMENT_ASSISTANT_PERSONA`) to maintain a helpful, polite, and strictly civic-focused tone.
- **Multilingual Support:** Automatically detects the language of the user's input and replies in the same language without requiring manual translation layers.
- **Government Scheme Guidance:** Distills complex scheme details into digestible bullet points.
- **Document Assistance:** Clearly lists exact documents required for specific applications.
- **Eligibility Questions:** Proactively asks follow-up questions if the user hasn't provided enough information to determine their eligibility.

### 📝 Complaint Reporting
- **Purpose:** A frictionless portal for citizens to report local infrastructure and civic issues.
- **AI Complaint Categorization:** The AI reads the natural language complaint and automatically tags it into strict predefined categories (e.g., `Road & Infrastructure`, `Electricity`, `Sanitation`).
- **Severity Detection:** Intelligently assigns `High`, `Medium`, or `Low` severity based on the context (e.g., live exposed wires = High).
- **Location Extraction:** Extracts addresses, landmarks, and city names automatically from unstructured text.
- **Complaint Tracking:** Allows citizens to view all logged complaints.
- **Persistent Storage:** Safely persists categorized complaints into a local `complaints.json` database.

### 🎯 Scheme Recommendation
- **Purpose:** Personalized welfare scheme discovery.
- **Citizen Profiling:** Takes simple demographic inputs (Age, Occupation, Income, State).
- **Eligibility Matching:** The AI cross-references the user's profile against all available government schemes to find the top 3 matches.
- **Recommendation Reasoning:** Explicitly explains *why* the user qualifies, building trust and clarity.
- **Required Documents:** Extracts and highlights the exact paperwork the citizen needs to gather.

---

## 4. Architecture

CivicAI operates on a highly decoupled, modular client-server architecture.

```text
       [ User Interface ]
       React Frontend (Vite)
                │
                ▼ (REST API / StandardResponse)
                │
       [ Backend Server ]
         FastAPI Engine
                │
                ▼ (Services Layer)
                │
    ┌───────────┴───────────┐
    │                       │
[ Business Logic ]     [ AI Service ]
ComplaintService       AIService Layer
SchemeService               │
    │                       ▼ (Prompt Fragments & Retry Logic)
    │                       │
[ Storage ]          [ Google Gemini AI ]
complaints.json      gemini-2.5-flash
schemes.json                │
    │                       ▼ (Clean JSON Parsing)
    └───────────┬───────────┘
                │
                ▼
      [ Client Response ]
```

**Layer Explanation:**
- **React Frontend:** Provides a responsive, accessible, and interactive user experience.
- **FastAPI Backend:** Handles routing, request validation (Pydantic), structured logging, and global error handling.
- **Business Services:** Isolates core logic for schemes and complaints away from HTTP routes.
- **AI Service:** A dedicated wrapper around the official `google-genai` SDK handling exponential backoff, timeouts, and JSON extraction.
- **Storage:** Lightweight persistent JSON stores for a portable MVP.

---

## 5. Folder Structure

```text
civic_ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # App entrypoint, middleware, logging, exception handlers
│   │   ├── config.py            # Centralized environment configuration
│   │   ├── models/              # Pydantic schemas (Request/Response models)
│   │   ├── routes/              # FastAPI routers (chat.py, complaints.py, recommend.py)
│   │   ├── services/            # Core business logic (ai_service.py, complaint_service.py)
│   │   ├── prompts/             # Reusable Gemini prompt templates and fragments
│   │   └── utils/               # Utility functions (e.g., json loading)
│   ├── data/                    
│   │   └── schemes.json         # Static mock dataset of government schemes
│   ├── complaints.json          # Auto-generated persistence file for complaints
│   └── .env                     # Environment variables
└── frontend/
    ├── src/
    │   ├── components/          # Modular React UI Components (Chat, Complaint, Recommendation)
    │   ├── services/            # API Client wrappers (api.js)
    │   ├── App.jsx              # Main React application layout
    │   └── index.css            # Global CSS and UI styling
    └── index.html               # HTML entry template
```

---

## 6. Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, CSS3 |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic |
| **AI Engine** | Google Gemini 2.5 Flash (`google-genai` SDK) |
| **Language** | JavaScript (ES6+), Python |
| **Libraries** | Axios (via native `fetch`), ContextVars |
| **Development**| npm, pip, virtualenv |

---

## 7. Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/CivicAI.git
cd CivicAI
```

### 2. Configure Backend
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Backend
```bash
uvicorn app.main:app --reload
# API will run on http://localhost:8000
```

### 5. Configure & Run Frontend
```bash
# Open a new terminal
cd frontend
npm install
npm run dev
# Frontend will run on http://localhost:5173
```

Open your browser to the Vite local URL to experience CivicAI.

---

## 8. Environment Variables

The backend relies heavily on the `GEMINI_API_KEY`.

- **`GEMINI_API_KEY`**: This is your private authentication key from Google AI Studio. 
  - **Example:** `GEMINI_API_KEY=AIzaSyA...xyz`
  - **Validation:** The application validates this key natively on startup. If it is missing, CivicAI will explicitly log a critical warning and gracefully disable AI endpoints with a `503 Service Unavailable` status rather than crashing.

---

## 9. API Endpoints

CivicAI standardizes all API responses inside a `StandardResponse` wrapper:
`{ "success": boolean, "message": string, "data": object }`

### `POST /chat/`
- **Purpose:** Converse with the AI assistant.
- **Request:** `{ "message": "What is PM Kisan?", "history": [...] }`
- **Response:**
  ```json
  {
    "success": true,
    "message": "Chat generated successfully.",
    "data": { "reply": "PM Kisan is a central sector scheme..." }
  }
  ```

### `POST /complaints/`
- **Purpose:** File a new complaint. The AI automatically parses severity, location, and category.
- **Request:** `{ "complaint": "Huge pothole on Anna Salai causing traffic." }`
- **Response:**
  ```json
  {
    "success": true,
    "message": "Complaint filed successfully.",
    "data": { "id": "uuid", "category": "Road & Infrastructure", "severity": "High" }
  }
  ```

### `GET /complaints/`
- **Purpose:** Retrieve all persistent complaints.
- **Response:** Array of Complaint objects inside `data`.

### `PATCH /complaints/{id}`
- **Purpose:** Update the resolution status of a specific complaint (e.g., `Resolved`).

### `POST /recommend/`
- **Purpose:** Get AI-driven scheme recommendations based on user demographics.
- **Request:** `{ "age": 30, "occupation": "Farmer", "monthly_income": 15000, "state": "Tamil Nadu" }`
- **Response:** Array of top 3 matching schemes with reasoning and required documents.

---

## 10. AI Design

- **Prompt Engineering:** Prompts are modularized in `base_prompt.py`. This allows us to share `JSON_RULES_FRAGMENT` globally to strictly enforce JSON output without markdown across multiple features.
- **Temperature Control:** 
  - `Chat` runs at `0.5` for a conversational but grounded tone.
  - `Recommendations` run at `0.2` for strict, analytical profile matching.
  - `Complaints` run at `0.1` for absolute deterministic categorization.
- **JSON Enforcement:** We explicitly command the model to drop markdown blockticks and provide a strict output schema.
- **Hallucination Prevention:** The prompt injects `schemes.json` directly into the AI's context and commands: `"NEVER recommend schemes outside the provided list."`
- **Complaint Classification:** Uses a strict enum list in the prompt to force the AI to select categories like `Electricity` or `Water Supply` rather than inventing its own tags.

---

## 11. Data Flow

```text
1. User enters demographic data in the React Frontend.
2. React dispatches a POST request to FastAPI (`/recommend`).
3. FastAPI validates the request using Pydantic.
4. The `SchemeService` loads available schemes.
5. `AIService` constructs an optimized prompt and queries Gemini via `google-genai`.
6. Gemini responds with a structured JSON string.
7. The Backend Parser strips markdown via Regex, maps it to Python dictionaries, and wraps it in a `StandardResponse`.
8. The Frontend receives the HTTP 200 response and renders the Scheme Cards.
```

---

## 12. Screenshots

| Chat Assistant | Complaint Reporting | Scheme Recommendations |
| :---: | :---: | :---: |
| *(Add screenshot here)* | *(Add screenshot here)* | *(Add screenshot here)* |
| Natural language interactions. | AI extracting categories and severity. | Profile-based personalized matching. |

---

## 13. Error Handling

CivicAI treats error handling as a first-class feature:
- **Network Failures:** Standardized HTTP 502 / 500 errors mapped to friendly UI banners.
- **Gemini Timeout:** Strict `10s` (Chat) and `30s` (Recommend) bounds using `asyncio.wait_for`. Gracefully returns HTTP `504 Gateway Timeout`.
- **Invalid JSON:** If Gemini hallucinates malformed JSON, a Regex parser attempts to clean it. If it fails, it returns HTTP `422 Unprocessable Entity` rather than a server crash.
- **Validation:** Pydantic models automatically block invalid frontend requests with `400 Bad Request`.

---

## 14. Performance Optimizations

- **Reduced Token Usage:** The Chat history dynamically slices to only retain the last 5 messages. The Recommendation flow strips out heavy textual descriptions, sending only critical `name` and `eligibility` keys to Gemini.
- **Async Requests:** Utilizes `asyncio.to_thread` to prevent the synchronous Gemini SDK from blocking the FastAPI event loop, ensuring the server handles concurrent users seamlessly.
- **Retry Logic:** Implemented an automatic Exponential Backoff (`2 ** attempt`) retry mechanism for Gemini API rate limits or timeouts.
- **Structured Logging:** Utilizes `ContextVars` to inject a unique `request_id` into every log statement across the system, enabling complex production debugging.
- **Compact Prompts:** Reusable prompt fragments keep the application DRY (Don't Repeat Yourself) and lightweight.

---

## 15. Security

- **Environment Variables:** `GEMINI_API_KEY` is completely isolated in a `.env` file and excluded via `.gitignore`.
- **Input Validation:** FastAPI + Pydantic strictly sanitize and type-check all incoming POST requests.
- **No Prompt Injection:** System prompts are strictly ordered so user input is encapsulated at the end of the payload, reducing prompt injection attack surfaces.
- **Safe Parsing:** Uses robust `json.loads` over `eval()`.

---

## 16. Future Improvements

- [ ] **Voice Assistant:** Add speech-to-text allowing rural citizens to query schemes vocally.
- [ ] **OCR Document Upload:** Allow users to snap a photo of their ID to automatically pre-fill the recommendation profile.
- [ ] **Real Government APIs:** Connect the mock `schemes.json` directly to live open-government data endpoints.
- [ ] **RAG Integration:** Implement a Vector Database to query massive nationwide repositories instead of flat JSON.
- [ ] **GIS Maps:** Plot incoming complaints on a heat map for municipal administrators.
- [ ] **Admin Dashboard & Analytics:** Create a secure portal for government workers to resolve complaints.
- [ ] **Multilingual UI:** Provide native language toggles directly in the React interface.

---

## 17. Contributors

- **[Your Name]** - *Lead Developer / Architect* - [GitHub Profile](https://github.com/yourusername)

*(Interested in contributing? Feel free to open a Pull Request!)*

---

## 18. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
  <i>Built with ❤️ for better civic engagement.</i>
</div>
