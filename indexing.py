from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from pathlib import Path
import json

# --- carregar modelo de embeddings ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- ler arquivos ---
texts = []
files = []

input_path = Path(r"D:\\dev\\oracle_project\\arquivos_md")
for f in input_path.iterdir():
    if f.is_file() and f.suffix.lower() in {".md", ".txt"}:
        files.append(str(f.absolute()))
        with open(f, "r", encoding="utf-8") as fp:
            texts.append(fp.read())

# --- criar documentos LangChain ---
docs = [Document(page_content=t, metadata={"source": file}) for t, file in zip(texts, files)]

# --- embeddings LangChain (mesmo usado acima, só wrapper) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- criar FAISS store ---
vectorstore = FAISS.from_documents(docs, embedding=embeddings)

# --- salvar índice + documentos para inferência ---
vectorstore.save_local("faiss_index_folder")

# --- opcional: salvar apenas a lista de arquivos (metadata) também ---
# with open("metadata.json", "w", encoding="utf-8") as f:
#     json.dump(files, f, ensure_ascii=False, indent=2)

print("Indexação concluída. FAISS + metadados salvos em 'faiss_index_folder'.")
