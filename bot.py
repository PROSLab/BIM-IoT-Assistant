import streamlit as st

from agent import generate_response


def write_message(role, content, save=True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the BIM and IoT Chatbot! How can I help you?"},
    ]


def handle_submit(message):
    """
    Submit handler:

    You will modify this method to talk with an LLM and provide
    context using data from knowledge graphs, databases, etc..
    """

    # Handle the response
    with st.spinner('Thinking...'):
        response = generate_response(message)
        write_message('assistant', response)


for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)




# Get user input

if prompt := st.chat_input("What is up?"):
    write_message('user', prompt)
    handle_submit(prompt)
