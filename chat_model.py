from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

class ChatModel:
    
    FAISS_FILE_DIR = "D:\\dev\\oracle_project\\faiss_index_folder"

    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com",
            streaming=True,  
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.vectorstore = FAISS.load_local(
            folder_path= self.FAISS_FILE_DIR,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

    def invoke(self, question):
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            verbose=True,
        )

        return qa_chain.invoke({"question": question})
    
    
if __name__ == "__main__":
    model = ChatModel()
    model.invoke("Meu nome é leandro. pode me chamar assim")
    model.invoke("Qual é o objetivo do escopo?")
    model.invoke("Quais são as atividades do escopo?")
    model.invoke("qual o meu nome?")
    


