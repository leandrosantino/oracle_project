import streamlit as st
from chat_model import ChatModel
from langchain_core.callbacks.base import BaseCallbackHandler
from pprint import pprint
from langchain.callbacks.stdout import StdOutCallbackHandler
from chat_model import REPHRASE_TEXT

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
        self.in_rephrase = False
        self.state = state
        self.container = container
        
    def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        print("\n ===== LLM start ===== \n")
        if REPHRASE_TEXT in prompts[0]:
            print(prompts[0])
            self.in_rephrase = True
        
    def on_chain_end(self, run: any, **kwargs):
        self.in_rephrase = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.in_rephrase:
            return
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
            model.invoke(StreamlitCallbackHandler(st.session_state, container), user_input)
            st.session_state.temp = ""
            st.session_state.history = model.get_messages()
