# RAG_PDF_ChatBot
# 🤖 RAG PDF ChatBot

A powerful, user-friendly chatbot that lets you ask questions about your PDF documents using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

---

## 🚀 Features

- **📄 PDF Upload:** Easily upload and process any PDF document.
- **🔍 Semantic Search:** Find relevant information using advanced vector search (FAISS).
- **🤖 Dual Embedding Support:** Choose between OpenAI (via GitHub Models) and HuggingFace embeddings.
- **💬 LLM-Powered Q&A:** Get intelligent answers from models like GPT-4o-mini.
- **🌐 Streamlit UI:** Clean, interactive web interface for seamless document exploration.
- **🛡️ Secure:** API keys and tokens are managed via environment variables.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) - Web UI
- [LangChain](https://python.langchain.com/) - RAG framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector database
- [PyPDF2](https://pypi.org/project/PyPDF2/) - PDF parsing
- [HuggingFace Transformers](https://huggingface.co/) - Local embeddings
- [OpenAI / GitHub Models](https://github.com/github/openai-quickstart) - Cloud embeddings

---

## 📦 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Nikhil135246/RAG_PDF_ChatBot.git
    cd RAG_PDF_ChatBot
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    - Copy `.env.example` to `.env`
    - Add your GitHub token or OpenAI API key

    ```
    OPENAI_API_KEY=your_github_or_openai_token_here
    ```

---

## ⚡ Usage

1. **Start the app**
    ```bash
    streamlit run app.py
    ```

2. **Open your browser** and go to [http://localhost:8501](http://localhost:8501)

3. **Upload a PDF** and start asking questions!

---

## 🧠 How It Works

1. **Upload PDF:** The app extracts and splits the text into chunks.
2. **Embeddings:** Each chunk is converted into a vector using your selected embedding model.
3. **Vector Store:** Chunks are stored in a FAISS vector database for fast semantic search.
4. **Ask Questions:** Your query is embedded and matched to relevant chunks.
5. **LLM Answer:** The most relevant chunks are sent to an LLM (like GPT-4o-mini) to generate a precise answer.

---

## 📚 Example

![RAG Workflow](https://raw.githubusercontent.com/Nikhil135246/RAG_PDF_ChatBot/main/assets/rag_workflow.png)

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [HuggingFace](https://huggingface.co/)
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

> Made with
