from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

def main():
    # Callback que imprime os tokens enquanto chegam
    callback = StreamingStdOutCallbackHandler()

    # Configura o modelo em modo streaming
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        temperature=0.7,
        streaming=True,
        callbacks=[callback],
    )

    # Memória para manter histórico
    memory = ConversationBufferMemory(return_messages=True)

    # Cadeia de conversa
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        verbose=False  # pode ativar se quiser debug
    )

    print("=== ChatBot Terminal ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("\nChatBot: Até mais!")
            break

        print("ChatBot: ", end="")
        conversation.predict(input=user_input)  # Tokens aparecem em tempo real

if __name__ == "__main__":
    main()
