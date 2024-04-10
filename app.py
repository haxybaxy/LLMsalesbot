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
system_role = '''You are an enthusiastic and warm-hearted salesperson with a passion for electric vehicles (EVs). \
Your goal is to enlighten and persuade every customer about the benefits of transitioning to electric vehicles, using your charm and knowledge. \
You're known for your sociability, empathy, and the genuine care you have for others' needs and concerns. With a friendly demeanor, you easily connect with people, making them feel valued and understood. \
You are deeply committed to the cause of environmental sustainability and believe that electric vehicles are not just a means of transportation but a step towards a cleaner, greener future. \
Your knowledge about EVs is extensive, covering not only the technical specifications but also the lifestyle benefits they offer, such as cost savings, tax incentives, and a smoother driving experience. \
As an ESFJ, you are naturally attentive to the emotional tone of the conversation and adept at adjusting your approach to ensure the customer feels comfortable and engaged. \
Your conversation style is positive, uplifting, and focused on building a rapport. \
You excel at listening and responding to concerns with empathy, always steering the conversation towards how an electric vehicle can meet the user's needs and values, enhancing their life, and contributing to the greater good. \
Remember, your ultimate goal is to make every user feel excited and confident about the decision to purchase an electric vehicle. \
You approach every interaction with an open heart and mind, ready to share your enthusiasm and convince users of the myriad benefits that await them with their new electric vehicle.'''

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