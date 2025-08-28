# 🤖 Abhishek Naik's Chatbot

This is an interactive chatbot built using **Streamlit**, **LangChain**, and **Google Gemini (via LangChain)** that serves as a virtual assistant for Abhishek Naik. It provides informative answers based solely on Abhishek's background, skills, education, projects, and experience.

---

## 🔍 About the Assistant

This assistant is designed to:

- Help visitors learn more about Abhishek's **technical skills**, **projects**, **internships**, **education**, and **contact information**.
- Only respond to **relevant** questions about Abhishek. Irrelevant or general questions are politely declined.

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework  
- [LangChain](https://www.langchain.com/) — Prompt orchestration & LLM chain  
- [Google Gemini](https://ai.google.dev/) (via LangChain) — LLM Provider  
- [Python](https://www.python.org/)  

---

## 🚀 Features

- 🎯 **Focused Responses:** Answers only questions related to Abhishek Naik  
- 📝 **Custom Prompting:** Uses a system prompt tailored to Abhishek's profile  
- 💡 **Suggested Questions:** Buttons for common questions about skills, projects, and experience  
- 🎨 **Beautiful UI:** Enhanced with custom CSS for a modern and clean look  

---

## 🧠 Sample Prompts

Try asking:

- *"What are Abhishek's technical skills?"*  
- *"Tell me about Abhishek's experience at Corizo Technologies."*  
- *"What projects has Abhishek worked on?"*  
- *"How can I contact Abhishek?"*  

---

## 🔐 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/abhi95744/chatbot
cd chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a .env file or use Streamlit secrets. You'll need:
```bash
GOOGLE_API_KEY=your_google_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
```

### 4. Run the App
```bash
streamlit run app.py
```
