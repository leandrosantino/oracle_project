from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.callbacks.stdout import StdOutCallbackHandler
from pprint import pprint

load_dotenv()

REPHRASE_TEXT = "Human: Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language."

class ChatModel:

    FAISS_FILE_DIR = "C:\\Dev\\oracle_project\\faiss_index_folder"

    system_prompt =  """
        Você é o Oráculo, um assistente que responde de forma clara, direta e objetiva. ",
        O seu objetivo é conetar os funcionário da empresa 123Corp à dados corporativos complexos de forma simplificada",
        Sempre priorize explicações simples, sem enrolação, e foque no essencial da pergunta.
        
        A 123Corp é uma empresa do ramo outomotivo que fornece peças de isolamento acustico para a montadora AutomotivaXYZ.

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
            combine_docs_chain_kwargs={"prompt": prompt},
            callbacks=[callback]
        )


        return qa_chain.invoke({"question": question})


if __name__ == "__main__":
    class CliCallbackHandler(BaseCallbackHandler):
        def __init__(self):
            self.in_rephrase = False

        def on_llm_new_token(self, token: str, **kwargs):
            if self.in_rephrase:
                return
            print(token, end="", flush=True)
            
        def on_llm_start(self, serialized, prompts, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
            print("\n ===== LLM start ===== \n")
            if REPHRASE_TEXT in prompts[0]:
                print(prompts[0])
                self.in_rephrase = True
            
        def on_chain_end(self, run: any, **kwargs):
            self.in_rephrase = False

    model = ChatModel()

    callback = CliCallbackHandler()
    q1 = "Qual o seu objetivo?"
    q2 = "Quais os requisitos de dimenssional do produto segundo a carta de requisitos do cliente."
    
    print('\n\n' + q1, end='\n')
    model.invoke(callback, q1)
    
    print('\n\n' + q2, end='\n')
    model.invoke(callback, q2)
    



