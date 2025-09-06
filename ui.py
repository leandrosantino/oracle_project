import streamlit as st
from chat_model import ChatModel
from langchain_core.callbacks.base import BaseCallbackHandler
import time

st.title("🔮 The Oracle", anchor="d")

@st.cache_resource()
def getModel():
    return ChatModel()

model = getModel()

if "history" not in st.session_state:
    st.session_state.history = model.get_messages()

user_input = st.chat_input("Pergunte alguma coisa")

if user_input:
    st.session_state.history.append({"type": "human", "content": user_input})

for msg in st.session_state.history:
    with st.chat_message(msg["type"]):
        st.markdown(msg["content"])
        
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, state, container):
        self.state = state
        self.container = container
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end='')    
        try:
            self.state.temp += token
            self.container.markdown(st.session_state.temp)
        except:
            print("failure")
                
st.session_state.temp = ""
if user_input:
    with st.chat_message("ai"):
        container = st.empty()
        with container:
            response = model.invoke(StreamlitCallbackHandler(st.session_state, container), user_input)
            st.session_state.temp = ""
            st.session_state.history = model.get_messages()

