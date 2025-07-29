from dotenv import load_dotenv
import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader  
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from openai import OpenAI

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

        # Embed the chunks using FREE HuggingFace embeddings
        try:
            st.write("🔄 Creating embeddings with HuggingFace (this may take a moment for first download)...")
            
            # Use free HuggingFace embeddings - much better than hash-based!
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}  # Use CPU (works on all machines)
            )
            
            knowledge_base = FAISS.from_texts(chunks, embeddings) 
            st.write("✅ Knowledge base created successfully!")
            
            # Show detailed embedding information
            st.write("**📊 Knowledge Base Details:**")
            st.write(f"- **Total vectors stored:** {knowledge_base.index.ntotal}")
            st.write(f"- **Vector dimension:** {knowledge_base.index.d}")
            st.write(f"- **Number of chunks:** {len(chunks)}")
            st.write("- **Embedding model:** HuggingFace all-MiniLM-L6-v2 (FREE & High Quality)")
            
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
            st.write("**If you see a download error:**")
            st.write("- Make sure you have internet connection")
            st.write("- The model downloads automatically on first use")
            st.write("- Try restarting the app")

if __name__ == "__main__":
    main()