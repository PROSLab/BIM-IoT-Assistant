##LLM configuration file
import streamlit as st
from langchain_openai import ChatOpenAI

print("Running with model: " + st.secrets["LLM_MODEL"])

# Configurazione OpenRouter
anthropic_claude_model = ChatOpenAI(
    model=st.secrets["LLM_MODEL"],
    openai_api_key=st.secrets["LLM_API_KEY"],
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=float(st.secrets["LLM_TEMPERATURE"]),
    default_headers={
        "HTTP-Referer": "http://localhost:8501", # Obbligatorio per OpenRouter (tua app)
        "X-Title": "BIM-IoT-Assistant",          # Obbligatorio per OpenRouter
    }
)