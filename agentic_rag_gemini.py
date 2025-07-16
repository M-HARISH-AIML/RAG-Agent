import os
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("""GOOGLE_API_KEY=your_google_api_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
""")
    print("✅ .env file created. Please edit it and add your credentials.")
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
email_user = os.getenv("EMAIL_ADDRESS")
email_pass = os.getenv("EMAIL_PASSWORD")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")
genai.configure(api_key=api_key)
import pyttsx3
import smtplib
from email.message import EmailMessage
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("❌ Failed to speak:", str(e))
def send_email():
    print("\n📧 Let's send an email.")
    to = input("Enter recipient email: ").strip()
    subject = input("Enter subject: ").strip()
    body = input("Enter body text: ").strip()

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", str(e))
def load_all_documents_from_folder(folder="data"):
    all_docs = []
    for file in Path(folder).glob("*.txt"):
        loader = TextLoader(str(file))
        all_docs.extend(loader.load())
    return all_docs
def create_rag_qa_chain():
    docs = load_all_documents_from_folder("data")
    if not docs:
        print("⚠️ No documents found in 'data' folder.")
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    if not chunks:
        print("⚠️ Document chunks are empty. Check your text files.")
        return None

    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(chunks, embedding)
    retriever = db.as_retriever()

    prompt_template = """
    Use the following context to answer the question. If the answer is not in the context, say you don't know.

    Context:
    {context}

    Question:
    {question}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0.2,
        convert_system_message_to_human=True
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )
def agentic_assistant():
    rag_chain = create_rag_qa_chain()
    if rag_chain is None:
        print("❌ Agent setup failed. Fix document loading issues and rerun.")
        return

    while True:
        print("\n🤖 What would you like to do?")
        print("1. Ask a question from document (RAG)")
        print("2. Speak some text")
        print("3. Send an email")
        print("4. Exit")
        choice = input("Enter option (1/2/3/4): ").strip()

        if choice == "1":
            query = input("Enter your question for the document: ").strip()
            try:
                result = rag_chain.invoke(query)
                print("\n💬 Answer:", result)
            except Exception as e:
                print("❌ Gemini API failed:", str(e))
        elif choice == "2":
            text = input("Enter text to speak: ").strip()
            speak_text(text)
            print("🔊 Text spoken!")
        elif choice == "3":
            send_email()
        elif choice == "4":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")
if __name__ == "__main__":
    agentic_assistant()
