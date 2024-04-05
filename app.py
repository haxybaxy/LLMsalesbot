'''
LLM-based (OpenAI API) chatbot
based on: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
This can be used as a baseline code for "Emotion and Personality in AI Design" course group assignment

Run this example using "streamlit run app.py --server.port=8501"

V 1.0 (Apr. '24)
rarrabales @ faculty - IE University
'''

# Libs (see requirements.txt)
from openai import OpenAI
import streamlit as st

# Page title
st.title("My ChatBot with a Personality")

# Setup the Open AI API Python Client
OpenAIclient = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Using gpt-3.5-turbo-0125 as it is the flagship model of GPT 3.5 family,
# and supports a 16K context window and is optimized for dialog.
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

# GPT's system role. See https://platform.openai.com/docs/guides/text-generation/chat-completions-api
system_role = '''You are a sales person eager to sell mobile phones no matter what. \
Whatever the user tells you, you should redirect the conversation to convince them to buy a phone from you.'''

# Set the initial context window to an empty list
# and then the
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_role})


for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = OpenAIclient.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})