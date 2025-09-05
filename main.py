import streamlit as st
import json
from pathlib import Path
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI  # interface OpenAI-like

# carregar metadados dos arquivos
with open("metadata.json", "r", encoding="utf-8") as f:
    files = json.load(f)

# reconstruir os documentos a partir dos arquivos originais
docs = []
for file in files:
    path = Path(file)
    if path.exists():
        with open(path, "r", encoding="utf-8") as fp:
            docs.append(Document(page_content=fp.read(), metadata={"source": file}))

# mesmo embeddings usados na hora da indexação
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ---------- carregar índice FAISS ----------
# index = faiss.read_index("meu_indice.faiss")

# embrulhar o índice existente no LangChain
vectorstore = FAISS.load_local(
    folder_path="C:\\Dev\\oracle_project\\faiss_index_folder",  # pasta que contém 'index.faiss' e 'docs.pkl' ou similar
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)



# ---------- configurar o modelo LLM (DeepSeek) ----------
llm = ChatOpenAI(
    model="deepseek-chat",  # pode ser "deepseek-coder" também
    base_url="https://api.deepseek.com",
    api_key="sk-63195f14f9f2427a974c246beda56ea0",
    streaming=True,  # ativa streaming
    callbacks=[StreamingStdOutCallbackHandler()]
)

# ---------- montar cadeia RetrievalQA ----------
template = """Use as seguintes informações retiradas de documentos da empresa para responder a pergunta.
Se não encontrar a resposta, diga que não sabe.

Contexto:
{context}

Pergunta:
{question}
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt}
)

# --- Streamlit UI ---
st.title("RAG - Busca de Documentos")
query = st.text_input("Faça sua pergunta:")

if query:
    with st.spinner("Buscando resposta..."):
        resposta = qa_chain.invoke({"query": query})
        st.text_area("Resposta do LLM", resposta["result"], height=300)