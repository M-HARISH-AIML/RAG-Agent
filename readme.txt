🤖 Agentic RAG Gemini Assistant
An intelligent, voice-capable assistant powered by Google Gemini, LangChain, and FAISS. It performs RAG (Retrieval-Augmented Generation), text-to-speech, and email-sending from a single interface.

🧩 Features
📖 Ask questions from uploaded .txt documents (RAG)

🗣️ Speak text aloud using pyttsx3

📧 Send emails using Gmail SMTP (or any SMTP provider)

🔐 Credentials stored securely via .env

🚀 Setup Instructions
1. 📁 Clone or download this repo
Make sure your project folder includes:

diff
Copy
Edit
- agentic_rag_gemini.ipynb (or .py)
- data/                ← place your .txt files here
- .env                 ← auto-generated with keys
2. 🛠 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Or manually from notebook:

python
Copy
Edit
!pip install langchain langchain-community langchain-google-genai google-generativeai \
faiss-cpu pyttsx3 email-validator chromadb python-dotenv
🔐 3. Setup your .env file
This is auto-generated, but make sure you update it like this:

ini
Copy
Edit
GOOGLE_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_gmail_app_password
✅ Must enable 2FA in Google and create an App Password

📂 4. Add Your Data
Place any .txt documents you want the assistant to read in the data/ folder.

▶️ 5. Run the Assistant
From terminal:

bash
Copy
Edit
python agentic_rag_gemini.py
Or run the notebook cell-by-cell in Jupyter.

📋 Available Actions
When the agent starts, choose an option:

markdown
Copy
Edit
1. Ask a question from document (RAG)
2. Speak some text
3. Send an email
4. Exit
💡 Examples
Ask: "What is artificial intelligence?" (if your document covers AI)

Speak: "Hello, Harish!"

Email: Send to anyone using Gmail credentials

🧠 Powered By
LangChain

Google Generative AI (Gemini)

FAISS

pyttsx3

smtplib

