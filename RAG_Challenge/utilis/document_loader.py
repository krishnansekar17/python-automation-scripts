import os
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile

class DocumentLoaderWithOCR:
    """Document loader with OCR capabilities for images in PDFs"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf_with_ocr(self, file_path: str) -> List[Document]:
        """Load PDF with OCR support for images"""
        documents = []
        
        try:
            # First, try standard PDF text extraction
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # Check if text extraction was successful
            total_text = "".join([doc.page_content for doc in docs])
            
            if len(total_text.strip()) < 100:  # Likely image-based PDF
                print("📸 Detected image-based PDF. Running OCR...")
                documents = self._ocr_pdf(file_path)
            else:
                documents = docs
                
        except Exception as e:
            print(f"⚠️ Standard extraction failed: {e}. Trying OCR...")
            documents = self._ocr_pdf(file_path)
        
        return documents
    
    def _ocr_pdf(self, file_path: str) -> List[Document]:
        """Perform OCR on PDF pages"""
        documents = []
        
        try:
            # Convert PDF to images
            images = convert_from_path(file_path, dpi=300)
            
            for page_num, image in enumerate(images, start=1):
                # Perform OCR
                text = pytesseract.image_to_string(image, lang='eng')
                
                # Create document
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": file_path,
                        "page": page_num,
                        "extraction_method": "ocr"
                    }
                )
                documents.append(doc)
                
            print(f"✅ OCR completed for {len(documents)} pages")
            
        except Exception as e:
            print(f"❌ OCR failed: {e}")
            raise
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def process_pdf(self, file_path: str) -> List[Document]:
        """Complete pipeline: load and split PDF"""
        print(f"📄 Processing: {file_path}")
        
        # Load with OCR support
        documents = self.load_pdf_with_ocr(file_path)
        
        # Split into chunks
        chunks = self.split_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks from {len(documents)} pages")
        
        return chunks