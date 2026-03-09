LinguaAssist — Government Schemes AI

> Multilingual AI assistant for Indian Government Schemes — voice, text & document support in 50+ languages

About The Project

LinguaAssist is a multilingual AI-powered web application that helps Indian citizens — especially rural and semi-urban populations — discover, understand, and apply for government welfare schemes in their own language.

Built for people who face language and literacy barriers when accessing government benefits, LinguaAssist brings the power of modern AI to every citizen, in every language.

🚀 Features

- 🌐 **50+ Language Support** — Hindi, Tamil, Telugu, Bengali, Kannada, Malayalam, Urdu, Arabic and many more including regional dialects like Tulu, Bhili, Chhattisgarhi, Haryanvi and tribal languages
- 🤖 **AI-Powered Chat** — Powered by Llama 3.3 70B via Groq API for fast, accurate responses about any Indian government scheme
- 📡 **RAG Pipeline** — Live data fetched from myscheme.gov.in API for real-time, up-to-date scheme information
- 🎤 **Voice Input & TTS** — Speak your question, get a spoken reply back in your chosen language using browser Speech APIs
- ⌨️ **Multilingual Virtual Keyboard** — On-screen keyboard for 15+ scripts including Devanagari, Tamil, Telugu, Bengali, Arabic and more
- ⭐ **Smart Scheme Recommender** — Personalized scheme recommendations based on user profile (age, income, occupation, gender, social category)
- 📎 **Document Upload** — Upload PDFs or images; AI extracts text and answers scheme-related queries from your documents
- 📍 **Find Nearest Help Centre** — GPS-based interactive map with Google Maps links for nearest CSC, bank and post office
- 🔐 **User Authentication** — 3-step profile registration or guest session
- 💬 **Chat History** — Persistent sessions with quick-access history panel
- ↔️ **RTL Language Support** — Proper right-to-left rendering for Urdu, Arabic, Sindhi and Kashmiri

🛠️ Tech Stack

| Layer          |    Technology |

| Frontend       |    Streamlit + custom HTML/CSS/JS |
| AI Model       |    Llama 3.3 70B Versatile via Groq API |
| Vision/OCR     |    Llama 3.2 11B Vision |
| Data Source    |    myscheme.gov.in REST API |
| Maps           |    Leaflet.js + OpenStreetMap |
| Speech         |    Web Speech API |
| Auth & Storage |    Local JSON files |

Schemes Covered

🌾 Agriculture · 🏥 Health · 🏠 Housing · 📚 Education · 💼 Employment · 🛡️ Insurance · 👴 Social Security · 👩 Women Welfare · 🤝 SC/ST/OBC · 💻 Digital Literacy · ♿ Disability

**60+ schemes with built-in eligibility logic**

Run Locally

```bash
git clone https://github.com/kavisha19111/linguaassist.git
cd linguaassist
pip install streamlit groq requests pdfplumber python-dotenv
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run the app:
```bash
streamlit run app.py
```

---

🌍 Target Users

Farmers, daily wage workers, rural women, students, senior citizens and anyone who needs to access government benefits but faces language or literacy barriers.

🙏 Acknowledgements

- [Groq](https://groq.com) for ultra-fast LLM inference
- [myScheme.gov.in](https://www.myscheme.gov.in) for the schemes API
- [Streamlit](https://streamlit.io) for the web framework
- [Leaflet.js](https://leafletjs.com) for interactive maps
