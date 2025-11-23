"""
Streamlit App for Hybrid RAG + Knowledge Graph Assistant
"""
import streamlit as st
import logging
from pathlib import Path
import tempfile
from typing import Dict, Any
import os

from config.config import config
from pipelines.rag_pipeline import RAGPipeline
from pipelines.kg_pipeline import KGPipeline
from utils.hybrid_retriever import HybridRetriever

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Hybrid RAG + KG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stExpander {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    if 'kg_pipeline' not in st.session_state:
        st.session_state.kg_pipeline = None
    if 'hybrid_retriever' not in st.session_state:
        st.session_state.hybrid_retriever = None
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False
    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def initialize_system():
    """Initialize RAG and KG pipelines"""
    try:
        with st.spinner("🔄 Initializing system..."):
            # Initialize RAG Pipeline
            st.session_state.rag_pipeline = RAGPipeline()
            logger.info("RAG Pipeline initialized")
            
            # Initialize KG Pipeline
            st.session_state.kg_pipeline = KGPipeline()
            logger.info("KG Pipeline initialized")
            
            # Initialize Hybrid Retriever
            st.session_state.hybrid_retriever = HybridRetriever(
                st.session_state.rag_pipeline,
                st.session_state.kg_pipeline
            )
            logger.info("Hybrid Retriever initialized")
            
            st.session_state.system_initialized = True
            st.success("✅ System initialized successfully!")
            return True
            
    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        st.error(f"❌ System initialization failed: {str(e)}")
        return False

def process_document(uploaded_file):
    """Process uploaded PDF document"""
    try:
        with st.spinner("📄 Processing document..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            logger.info(f"Processing: {tmp_path}")
            
            # Process with RAG Pipeline
            chunks = st.session_state.rag_pipeline.process_document(tmp_path)
            st.info(f"✅ Created {len(chunks)} chunks from {uploaded_file.name}")
            
            # Add to vector store
            st.session_state.rag_pipeline.create_from_documents(chunks)
            st.info(f"✅ Added {len(chunks)} chunks to vector store")
            
            # Setup QA chain
            st.session_state.rag_pipeline.setup_qa_chain()
            st.info("✅ QA chain setup successfully")
            
            # Process with KG Pipeline
            st.session_state.kg_pipeline.process_document(tmp_path)
            
            # Get KG stats
            stats = st.session_state.kg_pipeline.get_graph_stats()
            st.info(f"✅ Knowledge Graph built: {stats['num_nodes']} entities, {stats['num_relationships']} relations")
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            st.session_state.document_processed = True
            st.success("✅ Document processed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"Document processing failed: {e}")
        st.error(f"❌ Error processing file: {str(e)}")
        return False

def display_hybrid_results(results: Dict[str, Any]):
    """Display hybrid retrieval results in a nice format"""
    
    # Display RAG Results
    with st.expander("📚 Vector Store (RAG) Results", expanded=True):
        if results.get("rag_answer"):
            st.markdown("**Answer:**")
            st.info(results["rag_answer"])
            
            # Display sources
            if results.get("rag_sources"):
                st.markdown("**📄 Sources:**")
                for i, source in enumerate(results["rag_sources"], 1):
                    # Extract source information safely
                    source_file = source.get('source', 'Unknown')
                    page = source.get('page', 'N/A')
                    
                    # Display source info
                    st.markdown(f"""
                    **Source {i}:**
                    - 📄 File: `{Path(source_file).name if source_file != 'Unknown' else 'Unknown'}`
                    - 📖 Page: `{page}`
                    """)
        else:
            st.warning("No RAG results available")
    
    # Display Knowledge Graph Results
    with st.expander("🕸️ Knowledge Graph Results", expanded=True):
        if results.get("kg_answer"):
            st.markdown("**Answer:**")
            st.success(results["kg_answer"])
            
            # Display entities
            if results.get("kg_entities"):
                st.markdown("**🏷️ Related Entities:**")
                entities_text = ", ".join([f"`{e}`" for e in results["kg_entities"][:10]])
                st.markdown(entities_text)
            
            # Display relationships
            if results.get("kg_relations"):
                st.markdown("**🔗 Key Relationships:**")
                for i, rel in enumerate(results["kg_relations"][:5], 1):
                    st.markdown(f"{i}. {rel}")
        else:
            st.warning("No Knowledge Graph results available")
    
    # Display Hybrid Score
    if results.get("confidence"):
        st.markdown("---")
        confidence = results["confidence"]
        if confidence == "high":
            st.success(f"✅ Confidence: {confidence.upper()}")
        elif confidence == "medium":
            st.warning(f"⚠️ Confidence: {confidence.upper()}")
        else:
            st.error(f"❌ Confidence: {confidence.upper()}")

def display_sidebar():
    """Display sidebar with configuration and controls"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Configuration status
        with st.expander("📋 Configuration", expanded=False):
            if config.validate():
                st.success("✅ Configuration valid")
            else:
                st.error("❌ Configuration invalid")
        
        st.markdown("---")
        
        # System initialization
        if not st.session_state.system_initialized:
            if st.button("🚀 Initialize System", use_container_width=True):
                initialize_system()
        else:
            st.success("✅ System Ready")
        
        st.markdown("---")
        
        # Document upload
        st.markdown("## 📤 Upload Textbook")
        uploaded_file = st.file_uploader(
            "Upload PDF file",
            type=['pdf'],
            help="Upload a PDF textbook to process"
        )
        
        if uploaded_file:
            st.info(f"📄 {uploaded_file.name}\n\n{uploaded_file.size / 1024 / 1024:.1f}MB")
            
            if st.button("📊 Process Document", use_container_width=True):
                if st.session_state.system_initialized:
                    process_document(uploaded_file)
                else:
                    st.error("⚠️ Please initialize system first!")
        
        st.markdown("---")
        
        # System information
        with st.expander("ℹ️ System Information", expanded=False):
            st.markdown(f"""
            **Models:**
            - LLM: `{config.LLM_MODEL}`
            - Embeddings: `{config.EMBEDDING_MODEL}`
            
            **Vector Store:**
            - Database: Neon Postgres
            - Collection: textbook_embeddings
            
            **Knowledge Graph:**
            - Database: Neo4j
            - Status: {'✅ Connected' if st.session_state.system_initialized else '❌ Not connected'}
            """)

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    st.markdown('<div class="main-header">📚 Hybrid RAG + Knowledge Graph Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent Textbook Q&A with Zero Hallucinations</div>', unsafe_allow_html=True)
    
    # Check if system is ready
    if not st.session_state.system_initialized:
        st.info("👈 Please initialize the system from the sidebar to get started!")
        return
    
    if not st.session_state.document_processed:
        st.info("👈 Please upload and process a document from the sidebar!")
        return
    
    # Chat interface
    st.markdown("## 💬 Ask Questions")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"**You:** {message['content']}")
        else:
            with st.chat_message("assistant"):
                st.markdown("**Assistant:**")
                display_hybrid_results(message["content"])
    
    # Chat input
    question = st.chat_input("Enter your question:")
    
    if question:
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"**You:** {question}")
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    results = st.session_state.hybrid_retriever.query(question)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": results
                    })
                    
                    # Display results
                    st.markdown("**Assistant:**")
                    display_hybrid_results(results)
                    
                except Exception as e:
                    logger.error(f"Query failed: {e}")
                    st.error(f"❌ Error: {str(e)}")
        
        # Rerun to update chat display
        st.rerun()

if __name__ == "__main__":
    main()