import streamlit as st

st.set_page_config(page_title="🔮 The Oracle", layout="centered")
st.title("🔮 The Oracle")


if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Pergunte alguma coisa")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    
    response = """
        ## Olá!!
        **Leandro!**
        Seja ben vindo!
    """
    
    st.session_state.history.append({"role": "assistent", "content": response})
    

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
