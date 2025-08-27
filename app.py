import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

# Load on Streamlit Cloud, set in app settings
st.write("GOOGLE_API_KEY", st.secrets["GOOGLE_API_KEY"])
st.write("LANGCHAIN_TRACING_V2", st.secrets["LANGCHAIN_TRACING_V2"])
st.write("LANGCHAIN_API_KEY", st.secrets["LANGCHAIN_API_KEY"])


# Abhishek-only guard: constrain domain + refuse otherwise
SYSTEM_PROMPT = """You are a polite, helpful assistant for Abhishek Naik's personal website.

ABOUT ABHISHEK NAIK:
- Computer Engineering Graduate from C. V. Raman Global University (CGPA: 7.94, Aug 2020 – May 2024)
- Data Analyst with expertise in Python, SQL, and practical analytics
- Business Analyst Intern at Corizo Technologies (Sep 2024 – Nov 2024) and Acmegrade Pvt. Ltd. (Feb 2024 – May 2024)
- Skilled in: Python (90%), SQL (85%), Java (80%), JavaScript (75%), Node.js (75%), AWS (70%)
- Key Projects: CRM Pipeline Analytics, LangChain RAG Pipeline, Crypto Price Prediction, Home Inventory Manager
- Certifications: Hugging Face Agents, Salesforce Administrator, Cisco CCNA
- Location: Bhubaneswar, Odisha, India
- Contact: abhisheknaik2456@gmail.com, +91 6205302185
- LeetCode: https://leetcode.com/u/abhisheknaik2456/

Only answer questions that are about Abhishek (profile, skills, projects, experience, contact, education, certifications).
If a question is unrelated to Abhishek, reply briefly: 'This assistant only answers questions about Abhishek Naik.'

Provide detailed, helpful answers about Abhishek's background, skills, projects, and experience."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Question: {question}")
])

# Streamlit UI Configuration
st.set_page_config(
    page_title="Abhishek Chatbot", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
        max-width: 700px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 12px;
        color: white;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .chat-message {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
    }
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Abhishek Chatbot")
st.caption("Ask anything about Abhishek's profile, experience, projects, or skills.")

# Add some helpful prompts
st.markdown("**💡 Try asking about:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📝 Projects"):
        st.session_state.suggested_question = "Tell me about Abhishek's projects"
with col2:
    if st.button("🎯 Skills"):
        st.session_state.suggested_question = "What are Abhishek's technical skills?"
with col3:
    if st.button("💼 Experience"):
        st.session_state.suggested_question = "What is Abhishek's work experience?"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = ""

# Input handling
question = st.text_input(
    "Type a question about Abhishek:", 
    value=st.session_state.suggested_question,
    placeholder="e.g., What are Abhishek's key skills?",
    key="question_input"
)

# Clear suggested question after use
if st.session_state.suggested_question:
    st.session_state.suggested_question = ""

# Simple topicality check (extra safeguard)
def about_abhishek(q: str) -> bool:
    keywords = [
        "abhishek", "naik", "his", "profile", "resume", "cv", 
        "project", "projects", "experience", "skills", "skill", "contact", 
        "education", "university", "college", "degree", "certification",
        "work", "job", "intern", "internship", "company", "python", "sql",
        "java", "javascript", "aws", "data", "analyst", "crm", "langchain"
    ]
    q_low = q.strip().lower()
    return any(k in q_low for k in keywords) or len(q_low) < 5  # Allow short questions

# Process question
if question and question.strip():
    try:
        # Initialize LLM with error handling
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("⚠️ API key not configured. Please set GOOGLE_API_KEY in secrets.")
        else:
            with st.spinner("🤔 Thinking..."):
                # Gemini LLM via LangChain init_chat_model
                llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.3)
                output_parser = StrOutputParser()
                chain = prompt | llm | output_parser

                if about_abhishek(question):
                    answer = chain.invoke({"question": question})

                    # Display the conversation
                    st.markdown("**You asked:**")
                    st.markdown(f'<div class="chat-message">💭 {question}</div>', unsafe_allow_html=True)

                    st.markdown("**Abhishek's Assistant:**")
                    st.markdown(f'<div class="chat-message">🤖 {answer}</div>', unsafe_allow_html=True)

                else:
                    answer = "This assistant only answers questions about Abhishek Naik. Please ask about his profile, skills, projects, experience, or contact information."
                    st.markdown(f'<div class="chat-message error-message">❌ {answer}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        st.info("💡 This might be due to missing API configuration. Make sure GOOGLE_API_KEY is set in Streamlit secrets.")

# Footer
st.markdown("---")
st.markdown("**📧 Contact Abhishek:** abhisheknaik2456@gmail.com")
st.markdown("**🌐 Portfolio:** Built with passion for data and technology")
