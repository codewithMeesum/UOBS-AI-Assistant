# UOBS AI Assistant

AI-powered student services and academic admissions assistant for the **University of Baltistan, Skardu (UOBS)**.

## Features

- AI chat assistant for UOBS-related questions
- Quick prompts for common student topics
- Student LMS, Admissions Portal, and Official Website shortcuts
- Merit Aggregate Calculator
- Session-based chat history
- Local `.env` support
- Streamlit Secrets support for deployment

## Tech Stack

- Python
- Streamlit
- Google GenAI Python SDK
- python-dotenv
- Gemini API

## Project Structure

```text
UOBS-Chatbot/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

> The `.env` file is intentionally not included in GitHub because it contains the Gemini API key.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/UOBS-Chatbot.git
cd UOBS-Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

Create `.env` in the project folder:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 4. Run the app

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push `app.py`, `requirements.txt`, `README.md`, and `.gitignore` to GitHub.
2. Create a new app on Streamlit Community Cloud.
3. Select this repository and `app.py` as the main file.
4. Open the app's **Settings → Secrets**.
5. Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

6. Deploy.

The app checks `GEMINI_API_KEY` from the environment first, then Streamlit Secrets, so the same code works locally and after deployment.

## Security

Never upload your real Gemini API key to GitHub.

Keep `.env` local. The `.gitignore` file already excludes it.

## Notes

This is a student-built prototype demonstrating an AI-powered university support assistant. For current administrative information, users should verify important details through official UOBS channels.

## Author

**Meesum Mukhtar**  
BS Artificial Intelligence Student  
University of Baltistan, Skardu
