"""
Hybrid Retriever combining RAG and Knowledge Graph
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HybridRetriever:
    """Hybrid retriever combining RAG and KG pipelines"""
    
    def __init__(self, rag_pipeline, kg_pipeline):
        """Initialize hybrid retriever"""
        self.rag_pipeline = rag_pipeline
        self.kg_pipeline = kg_pipeline
        logger.info("Hybrid Retriever initialized")
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query both RAG and KG systems and combine results"""
        try:
            logger.info(f"🔍 Querying hybrid system: {question}")
            
            # Query RAG pipeline
            logger.info("📚 Querying Vector Store...")
            rag_result = self.rag_pipeline.query(question)
            
            # Query KG pipeline
            logger.info("🕸️ Querying Knowledge Graph...")
            kg_result = self.kg_pipeline.query_graph(question)
            
            # Combine results
            combined_result = {
                "rag_answer": rag_result.get("answer", ""),
                "rag_sources": rag_result.get("sources", []),
                "kg_answer": kg_result.get("answer", ""),
                "kg_entities": kg_result.get("entities", []),
                "kg_relations": kg_result.get("relations", []),
                "confidence": self._calculate_confidence(rag_result, kg_result)
            }
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Hybrid query failed: {e}")
            raise
    
    def _calculate_confidence(self, rag_result: Dict, kg_result: Dict) -> str:
        """Calculate confidence score based on both results"""
        try:
            # Simple confidence calculation
            has_rag = bool(rag_result.get("answer"))
            has_kg = bool(kg_result.get("answer"))
            has_sources = bool(rag_result.get("sources"))
            has_entities = bool(kg_result.get("entities"))
            
            score = sum([has_rag, has_kg, has_sources, has_entities])
            
            if score >= 3:
                return "high"
            elif score >= 2:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            logger.error(f"Confidence calculation failed: {e}")
            return "low"