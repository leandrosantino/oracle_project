from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.callbacks.stdout import StdOutCallbackHandler

load_dotenv()

class ChatModel:
    
    FAISS_FILE_DIR = "C:\\Dev\\oracle_project\\faiss_index_folder"
    
    system_prompt =  """
        Você é o Oráculo, um assistente que responde de forma clara, direta e objetiva. ",
        O seu objetivo é conetar os funcionário da empresa Adler Pelzer à dados corporativos complexos de forma simplificada",
        Sempre priorize explicações simples, sem enrolação, e foque no essencial da pergunta.
        
        Com base nesse Contexto:
        {context}

        responda a Pergunta:
        {question}
        
    """

    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.load_local(
            folder_path= self.FAISS_FILE_DIR,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        
    def get_messages(self):
        messages = []    
        for msg in self.memory.chat_memory.messages:
            messages.append({"type": msg.type, "content": msg.content})
            # print(f"{msg.type.upper()}: {msg.content}")
        return messages

    def invoke(self, callback: BaseCallbackHandler, question):
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com",
            streaming=True,  
            callbacks=[callback]
        )

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.system_prompt
        )
    
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            memory = self.memory,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            combine_docs_chain_kwargs={"prompt": prompt}
        )

        
        return qa_chain.invoke({"question": question})
    
    
if __name__ == "__main__":
    model = ChatModel()

    callback = StdOutCallbackHandler()
    
    print(model.invoke(callback, "Qual o seu objetivo"))
    print(model.invoke(callback, "me fala sobre o roejto faciliy"))
    


