"""
RAG Pipeline for document processing and retrieval
"""
import logging
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from config.config import config

logger = logging.getLogger(__name__)

class RAGPipeline:
    """RAG Pipeline for document processing and question answering"""
    
    def __init__(self):
        """Initialize RAG pipeline components"""
        try:
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                model=config.EMBEDDING_MODEL,
                openai_api_key=config.OPENAI_API_KEY
            )
            
            # Initialize vector store connection
            self.vector_store = None
            self.qa_chain = None
            
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP,
                length_function=len,
            )
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                model=config.LLM_MODEL,
                temperature=0,
                openai_api_key=config.OPENAI_API_KEY
            )
            
            logger.info("RAG Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Pipeline: {e}")
            raise
    
    def initialize_vector_store(self):
        """Initialize connection to Neon Postgres vector store with connection pooling"""
        try:
            # Add connection arguments for better stability
            connection_string = config.neon_connection_string
            
            # Ensure connection string has proper SSL mode
            if "sslmode" not in connection_string:
                connection_string += "?sslmode=require"
            
            # Add connection pooling parameters
            if "?" in connection_string:
                connection_string += "&connect_timeout=10&keepalives=1&keepalives_idle=30&keepalives_interval=10&keepalives_count=5"
            else:
                connection_string += "?connect_timeout=10&keepalives=1&keepalives_idle=30&keepalives_interval=10&keepalives_count=5"
            
            self.vector_store = PGVector(
                connection_string=connection_string,
                embedding_function=self.embeddings,
                collection_name="textbook_embeddings",
                pre_delete_collection=False,
            )
            logger.info("Vector store initialized with connection pooling")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def extract_text_with_ocr(self, pdf_path: str) -> str:
        """Extract text from PDF using OCR for scanned documents"""
        try:
            images = convert_from_path(pdf_path)
            text = ""
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                text += f"\n--- Page {i+1} ---\n{page_text}"
            return text
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def process_document(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Process PDF document and create embeddings"""
        try:
            # Try standard PDF extraction first
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # If no text extracted, use OCR
            if not documents or all(len(doc.page_content.strip()) < 50 for doc in documents):
                logger.info("Using OCR for text extraction")
                ocr_text = self.extract_text_with_ocr(pdf_path)
                from langchain.schema import Document
                documents = [Document(page_content=ocr_text, metadata={"source": pdf_path})]
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            logger.info(f"Processed {len(chunks)} chunks from document")
            return chunks
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add document chunks to vector store"""
        try:
            if not self.vector_store:
                self.initialize_vector_store()
            
            self.vector_store.add_documents(chunks)
            logger.info(f"Added {len(chunks)} chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def create_from_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """Create vector store from document chunks"""
        try:
            # Build connection string with proper parameters
            connection_string = config.neon_connection_string
            if "sslmode" not in connection_string:
                connection_string += "?sslmode=require"
            if "?" in connection_string and "connect_timeout" not in connection_string:
                connection_string += "&connect_timeout=10&keepalives=1&keepalives_idle=30"
            
            if not self.vector_store:
                # Create new vector store from documents
                self.vector_store = PGVector.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    connection_string=connection_string,
                    collection_name="textbook_embeddings",
                    pre_delete_collection=False,
                )
                logger.info(f"Created vector store with {len(chunks)} chunks")
            else:
                # Add to existing vector store
                self.vector_store.add_documents(chunks)
                logger.info(f"Added {len(chunks)} chunks to existing vector store")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create from documents: {e}")
            raise
    
    def setup_qa_chain(self):
        """Setup the QA chain for question answering"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized. Please process a document first.")
            
            # Create retrieval chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                return_source_documents=True,
            )
            
            logger.info("QA chain setup successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup QA chain: {e}")
            raise
    
    def query(self, question: str, k: int = 5, max_retries: int = 3) -> Dict[str, Any]:
        """Query the RAG system with retry logic"""
        for attempt in range(max_retries):
            try:
                if not self.vector_store:
                    raise ValueError("Vector store not initialized. Please upload a document first.")
                
                # Reinitialize vector store connection if needed
                if attempt > 0:
                    logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
                    self.initialize_vector_store()
                
                # Setup QA chain if not already done
                if not self.qa_chain or attempt > 0:
                    self.setup_qa_chain()
                
                # Get response using invoke (not __call__)
                response = self.qa_chain.invoke({"query": question})
                
                return {
                    "answer": response["result"],
                    "sources": [doc.metadata for doc in response["source_documents"]],
                    "confidence": "high"
                }
                
            except Exception as e:
                logger.error(f"Query attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                # Wait before retry
                import time
                time.sleep(1)
    
    def get_relevant_context(self, question: str, k: int = 5) -> List[str]:
        """Get relevant context chunks for a question"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            docs = self.vector_store.similarity_search(question, k=k)
            return [doc.page_content for doc in docs]
            
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return []