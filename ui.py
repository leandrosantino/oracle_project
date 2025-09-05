import streamlit as st
from chat_model import ChatModel
from langchain_core.callbacks.base import BaseCallbackHandler
import time
import threading

class ChatCallback(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_start(self, token: str):
        self.text += token
        self.container.markdown(self.text)
        print(token, end='')
    
data = st.empty()

@st.cache_resource
def getModel():
    model = ChatModel(ChatCallback(data))

    model.invoke({"role": "user", "content": "quem descobrio o brasil?"})
    
    return model


model = getModel()

st.set_page_config(page_title="🔮 The Oracle", layout="centered")
st.title("🔮 The Oracle")


if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Pergunte alguma coisa")
    

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    model.invoke(st.session_state.history)

for msg in st.session_state.history:
    if msg["role"] == "user":
        # Mensagem do usuário (direita)
        st.markdown(
            f"""
            <div style='text-align: right; display: flex; justify-content: end'>
                <div style='background-color: gray; padding: 10px; border-radius: 10px; margin: 5px 0; width: fit-content' >
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Mensagem do assistente (esquerda, com markdown)
        st.markdown(msg["content"])
