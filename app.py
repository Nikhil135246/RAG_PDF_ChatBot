from dotenv import load_dotenv
import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader  
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from openai import OpenAI

# Custom GitHub Models Embedding Class
class GitHubEmbeddings(Embeddings):
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.environ["OPENAI_API_KEY"],  # Your GitHub token
        )
        self.model_name = "openai/text-embedding-3-small"
    
    def embed_documents(self, texts):
        """Embed multiple documents"""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            st.error(f"GitHub embedding error: {e}")
            return []
    
    def embed_query(self, text):
        """Embed a single query"""
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.model_name,
            )
            return response.data[0].embedding
        except Exception as e:
            st.error(f"GitHub embedding error: {e}")
            return []

def main():
    load_dotenv()
    
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF💭")
    
    # Upload PDF file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        st.text_area("PDF Content", text, height=300)
        st.success("PDF loaded successfully!")

        # Split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=500,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        st.write(f"**📝 Text split into {len(chunks)} chunks**")
        
        # Show first few chunks
        for i, chunk in enumerate(chunks[:3]):
            with st.expander(f"Chunk {i+1}"):
                st.write(chunk)

        # Choose embedding method
        st.write("**🤖 Choose Embedding Method:**")
        embedding_choice = st.radio(
            "Select embedding service:",
            ["GitHub Models (OpenAI)", "HuggingFace (Local)"]
        )
        
        try:
            if embedding_choice == "GitHub Models (OpenAI)":
                st.write("🔄 Creating embeddings with GitHub Models...")
                embeddings = GitHubEmbeddings()
                embedding_info = "GitHub Models - OpenAI text-embedding-3-small (1536 dims)"
            else:
                st.write("🔄 Creating embeddings with HuggingFace...")
                from langchain_community.embeddings import HuggingFaceEmbeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                embedding_info = "HuggingFace all-MiniLM-L6-v2 (384 dims)"
            
            knowledge_base = FAISS.from_texts(chunks, embeddings) 
            st.write("✅ Knowledge base created successfully!")
            
            # Show detailed embedding information
            st.write("**📊 Knowledge Base Details:**")
            st.write(f"- **Total vectors stored:** {knowledge_base.index.ntotal}")
            st.write(f"- **Vector dimension:** {knowledge_base.index.d}")
            st.write(f"- **Number of chunks:** {len(chunks)}")
            st.write(f"- **Embedding model:** {embedding_info}")
            
            # Test similarity search
            st.write("**🔍 Test Your Knowledge Base:**")
            test_query = st.text_input("Enter a question to search in your PDF:")
            if test_query:
                try:
                    # Perform similarity search
                    docs = knowledge_base.similarity_search(test_query, k=3)
                    st.write(f"**Found {len(docs)} most relevant chunks:**")
                    for i, doc in enumerate(docs):
                        with st.expander(f"📄 Relevant Chunk {i+1}"):
                            st.write(doc.page_content)
                except Exception as search_error:
                    st.error(f"Search error: {search_error}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.write("**Troubleshooting:**")
            if "GitHub" in str(e):
                st.write("- Check your GitHub token in .env file")
                st.write("- Make sure you have internet connection")
            else:
                st.write("- Try switching to the other embedding method")

if __name__ == "__main__":
    main()