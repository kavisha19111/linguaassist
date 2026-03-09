

---

# 🌐 LinguaAssist — AI for Indian Government Schemes

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-LLM-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Languages-50+-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Schemes-60+-purple?style=for-the-badge"/>
</p>

> A multilingual AI-powered web application that helps every Indian citizen — especially rural and semi-urban populations — discover, understand and apply for government welfare schemes in their own language.

---

## 🧠 What Does This Do?

India has over 3,000 government welfare schemes — but most citizens, especially in rural areas, never benefit from them. The reasons? Language barriers, lack of awareness, complex application processes and no accessible guidance.

LinguaAssist solves this by combining the power of modern Large Language Models with real-time government data, voice interaction, and support for 50+ Indian and international languages — so that every citizen can ask about any scheme in their own language and get a clear, simple answer.

---

## 🚀 Features

### 🌐 Language & Communication
- **50+ Language Support** — Hindi, Tamil, Telugu, Bengali, Kannada, Malayalam, Urdu, Arabic and many more including rare regional dialects like Tulu, Bhili, Chhattisgarhi, Haryanvi, Kokborok and tribal languages
- **Voice Input & TTS** — Speak your question in your language, get a spoken reply back using browser Speech APIs
- **Multilingual Virtual Keyboard** — On-screen keyboard for 15+ scripts including Devanagari, Tamil, Telugu, Bengali, Arabic, Cyrillic and more
- **RTL Language Support** — Proper right-to-left rendering for Urdu, Arabic, Sindhi and Kashmiri

### 🤖 AI & Data
- **Llama 3.3 70B** — Ultra-fast, accurate responses powered by Groq API
- **RAG Pipeline** — Live data fetched from myscheme.gov.in API so responses are always up to date
- **Document Upload** — Upload PDFs or images of your documents; AI extracts text and answers scheme queries based on your actual documents
- **Vision OCR** — Llama 3.2 11B Vision model reads and understands uploaded document images

### ⭐ Personalisation
- **Smart Scheme Recommender** — After registration, the app analyses your profile (age, income, occupation, gender, social category, land holding) and recommends the most relevant schemes from 60+ options
- **Eligibility Logic** — Built-in rules for every scheme — only shows schemes you actually qualify for
- **Profile-Based Filtering** — Schemes grouped by category with relevance scores

### 📍 Location & Access
- **Find Nearest Help Centre** — GPS-based interactive Leaflet map that generates Google Maps links for the nearest CSC (Common Service Centre), bank and post office
- **Official Portal Links** — Direct links to CSC Locator and myScheme portal

### 🔐 User Experience
- **Authentication System** — 3-step profile registration with secure login or one-click guest session
- **Persistent Chat History** — Sessions saved locally with quick-access history panel
- **Quick Questions** — One-click common queries for instant answers
- **Dark UI** — Beautiful dark-themed interface optimised for low-end devices

---

## 📋 Schemes Database

| Category | Examples |
|----------|---------|
| 🌾 Agriculture | PM Kisan, Fasal Bima, Kisan Credit Card, PM-KUSUM |
| 🏥 Health | Ayushman Bharat PM-JAY, Janani Suraksha, NHM |
| 🏠 Housing | PM Awas Yojana Urban & Rural, CLSS |
| 📚 Education | NSP, Samagra Shiksha, Beti Bachao, Sukanya Samriddhi |
| 💼 Employment | MGNREGA, PM Mudra, Skill India, PM SVANidhi |
| 🛡️ Insurance | PM Jeevan Jyoti, PM Suraksha, Atal Pension |
| 👩 Women | Mahila Shakti Kendra, STEP, Ujjwala Yojana |
| 🤝 SC/ST/OBC | Sub-Plans, Scholarships, Fellowships |
| 💻 Digital | PM Gramin Digital Saksharta, BharatNet |
| ♿ Disability | ADIP Scheme, UDID |

**60+ schemes with built-in eligibility rules**

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit + custom HTML/CSS/JS |
| AI Model | Llama 3.3 70B Versatile via Groq API |
| Vision & OCR | Llama 3.2 11B Vision |
| Data Source | myscheme.gov.in REST API (RAG) |
| Maps | Leaflet.js + OpenStreetMap |
| Speech | Web Speech API (Recognition + Synthesis) |
| Auth & Storage | Local JSON |
| PDF Processing | pdfplumber |

---

## 🏗️ Architecture

```
User Input (Text / Voice / Document)
           ↓
    Language Detection
           ↓
   RAG — myscheme.gov.in API
           ↓
  Llama 3.3 70B via Groq API
           ↓
 Response in User's Language
           ↓
  TTS Spoken Reply (if voice)
```

---

## 📁 Project Structure

```
linguaassist/
│
├── app.py                  # Complete application — all logic,
│                           # UI, AI, maps, auth in one file
├── .gitignore              # Excludes sensitive files
└── README.md               # You are here
```

---

## 🏃 Run It Yourself

**1. Clone the repo**
```bash
git clone https://github.com/kavisha19111/linguaassist.git
cd linguaassist
```

**2. Install dependencies**
```bash
pip install streamlit groq requests pdfplumber python-dotenv
```

**3. Create a `.env` file**
```
GROQ_API_KEY=your_groq_api_key_here
```
👉 Get your free API key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
streamlit run app.py
```

---

## 🌍 Target Users

| User | How LinguaAssist Helps |
|------|----------------------|
| 👨‍🌾 Farmers | Discover PM Kisan, Fasal Bima, Kisan Credit Card in their language |
| 👩 Rural Women | Find Ujjwala, Mahila Shakti, Janani Suraksha schemes |
| 👴 Senior Citizens | Learn about pension schemes via voice in their language |
| 🎓 Students | Discover scholarships and education loans |
| 💼 Unemployed Youth | Find MGNREGA, Mudra, Skill India opportunities |
| ♿ Differently Abled | Access ADIP and UDID scheme information |

---

## 🔮 Future Improvements

- [ ] Replace JSON storage with PostgreSQL database for multi-user scalability
- [ ] Add WhatsApp Bot integration for feature phone users
- [ ] Offline mode with cached scheme data
- [ ] Add more Indian languages and dialects
- [ ] State-specific scheme filtering
- [ ] Integration with DigiLocker for document verification
- [ ] Deploy on cloud with proper authentication

---

## 📚 What I Learned

- Building production-grade multilingual NLP applications
- Integrating RAG pipelines with live government APIs
- Working with browser Speech APIs for voice interaction
- Implementing custom virtual keyboards for 15+ scripts
- Designing accessible UI for rural and low-literacy users
- Handling RTL languages and complex Unicode scripts
- GPS and map integration inside Streamlit iframes

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [myScheme.gov.in](https://www.myscheme.gov.in) — Government schemes API
- [Streamlit](https://streamlit.io) — Web framework
- [Leaflet.js](https://leafletjs.com) — Interactive maps
- [Meta AI](https://ai.meta.com) — Llama 3.3 model

---

<p align="center">
Built with ❤️ for 1.4 billion Indians — in their own language
</p>
