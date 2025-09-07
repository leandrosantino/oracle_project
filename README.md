<div align="center">  
  <h1>🔮 Oracle - AI Chat Assistant</h1>   
</div>  
<br>  

![Demo](/.examples/preview.png)

## 📌 Descrição  

O **Oracle** é um sistema de chat de inteligência artificial feito em **Python**, construído sobre o **LangChain** e conectado ao modelo **DeepSeek**. O objetivo é atuar como um **oráculo corporativo**, respondendo perguntas internas da empresa com base em informações confiáveis extraídas de documentos locais.

A ideia central é que o Oracle não seja apenas um chatbot genérico, mas sim uma ferramenta que **entende o contexto do negócio**. Para isso, ele combina **RAG (Retrieval Augmented Generation)** e **técnicas de Embeddings**, permitindo que o modelo de linguagem consulte documentos internos antes de formular uma resposta. Isso garante que as interações sejam embasadas em dados reais da empresa.

Com essa abordagem, o Oracle pode:

* Indexar e armazenar documentos da empresa (manuais, relatórios, políticas internas, etc.).
* Realizar buscas semânticas, indo além da simples correspondência de palavras-chave.
* Fornecer respostas contextuais, explicativas e alinhadas ao conteúdo real da organização.
* Servir como ponto único de consulta, acelerando a tomada de decisão e a comunicação interna.

<br>  

## 🚀 Tecnologias Utilizadas  

- **Python 3.11+**: Linguagem principal.  
- **LangChain**: Framework para orquestração da IA.  
- **Streamlit**: Interface web simples e interativa para interação com o oráculo.
- **RAG & Embeddings**: Para recuperação de informações de documentos locais.
- **DeepSeek API**: Modelo LLM conectado.

<br>  

## 📦 Como Executar o Projeto

### 1️⃣ Clonar o repositório

```sh
git clone https://github.com/seuusuario/oracle.git
cd oracle
```

### 2️⃣ Instalar dependências com **uv**

```sh
uv sync
```

### 3️⃣ Executar a aplicação com **Streamlit**

```sh
uv run streamlit run ui.py
```

Após rodar, a interface estará disponível em:
👉 [http://localhost:8501](http://localhost:8501)
