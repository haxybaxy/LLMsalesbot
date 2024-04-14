from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
import streamlit as st

embedding_function = OpenAIEmbeddings()
loader = JSONLoader(file_path="./EV_data.json", jq_schema=".electric_vehicles[]", text_content=False)
documents = loader.load()
db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()
template = """Answer the question based only on the following context: {context}\n\nQuestion: {question}"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()
chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | model | StrOutputParser())

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.empty()
        self.container.write(self.text)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    response_container = st.empty()
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(response_container)
        llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
        response = chain.invoke(prompt)
        response = response.replace("$","\$")
        response_container.write(response, markdown = False)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response))
