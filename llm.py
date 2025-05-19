##LLM configuration file
import streamlit as st
from langchain_anthropic import ChatAnthropic

anthropic_claude_model = ChatAnthropic(temperature=0,
                                       anthropic_api_key="ANTHROPIC_KEY",
                                       model_name="CHOOSE_MODEL",)

