"""
Knowledge Graph Pipeline for entity extraction and relationship building
"""
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase
import spacy

from config.config import config

logger = logging.getLogger(__name__)

class KGPipeline:
    """Knowledge Graph Pipeline for building and querying knowledge graphs"""
    
    def __init__(self):
        """Initialize KG pipeline components"""
        self.driver = None  # Initialize driver first
    
        try:
            # Initialize Neo4j connection
            self.driver = GraphDatabase.driver(
                config.neo4j_uri,
                auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
            )

            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
        
            logger.info("✅ Neo4j Knowledge Graph initialized")
        
            # Initialize NLP model for entity extraction
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found, downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")
        
            # Initialize LLM for entity extraction
            self.llm = ChatOpenAI(
                model=config.LLM_MODEL,
                temperature=0,
                openai_api_key=config.OPENAI_API_KEY
            )
        
            # Text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
        
            logger.info("KG Pipeline initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize KG Pipeline: {e}")
            # Clean up driver if initialization failed
            if self.driver:
                try:
                    self.driver.close()
                except:
                    pass
                self.driver = None
            raise
    
    def extract_entities_and_relations(self, text: str) -> Dict[str, Any]:
        """Extract entities and relationships from text using spaCy and LLM"""
        try:
            # Use spaCy for basic entity extraction
            doc = self.nlp(text[:100000])  # Limit text length
            
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            
            # Extract relationships using LLM
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                Extract key relationships from the following text.
                Format: Subject -> Relationship -> Object
                
                Text: {text}
                
                Relationships:
                """
            )
            
            # Get relationships from LLM
            relations = []
            if len(text) < 3000:  # Only use LLM for shorter texts
                try:
                    response = self.llm.invoke(prompt.format(text=text))
                    relations_text = response.content if hasattr(response, 'content') else str(response)
                    
                    # Parse relationships
                    for line in relations_text.split('\n'):
                        if '->' in line:
                            parts = line.split('->')
                            if len(parts) == 3:
                                relations.append({
                                    "subject": parts[0].strip(),
                                    "relation": parts[1].strip(),
                                    "object": parts[2].strip()
                                })
                except Exception as e:
                    logger.warning(f"LLM relation extraction failed: {e}")
            
            return {
                "entities": entities,
                "relations": relations
            }
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {"entities": [], "relations": []}
    
    def add_to_graph(self, entities: List[Dict], relations: List[Dict]):
        """Add entities and relationships to Neo4j graph with duplicate handling"""
        try:
            with self.driver.session() as session:
                entities_added = 0
                relations_added = 0
                
                # Add entities with MERGE (handles duplicates gracefully)
                for entity in entities:
                    try:
                        result = session.run(
                            """
                            MERGE (e:Entity {name: $name})
                            ON CREATE SET e.type = $type, e.created = timestamp()
                            ON MATCH SET e.type = $type, e.updated = timestamp()
                            RETURN e
                            """,
                            name=entity["text"],
                            type=entity["label"]
                        )
                        if result.single():
                            entities_added += 1
                    except Exception as e:
                        logger.debug(f"Entity already exists: {entity['text']}")
                        continue
                
                # Add relationships with MERGE (handles duplicates gracefully)
                for relation in relations:
                    try:
                        result = session.run(
                            """
                            MERGE (s:Entity {name: $subject})
                            MERGE (o:Entity {name: $object})
                            MERGE (s)-[r:RELATES {type: $relation}]->(o)
                            ON CREATE SET r.created = timestamp()
                            ON MATCH SET r.updated = timestamp()
                            RETURN r
                            """,
                            subject=relation["subject"],
                            object=relation["object"],
                            relation=relation["relation"]
                        )
                        if result.single():
                            relations_added += 1
                    except Exception as e:
                        logger.debug(f"Relation already exists")
                        continue
                
                logger.info(f"✅ Added/Updated {entities_added} entities and {relations_added} relations")
                
        except Exception as e:
            logger.error(f"Failed to add to graph: {e}")
            # Don't raise - allow processing to continue
            logger.warning("⚠️ Continuing despite graph errors...")


    def process_document(self, pdf_path: str):
        """Process PDF document and build knowledge graph"""
        try:
            # Load document
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            logger.info(f"Processing {len(chunks)} chunks for KG")
            
            all_entities = []
            all_relations = []
            
            # Process each chunk
            for i, chunk in enumerate(chunks):
                if i % 20 == 0:
                    logger.info(f"📊 Processing document {i}/{len(chunks)}...")
                
                result = self.extract_entities_and_relations(chunk.page_content)
                all_entities.extend(result["entities"])
                all_relations.extend(result["relations"])
                
                # Add to graph in batches to avoid memory issues
                if len(all_entities) >= 100:
                    self.add_to_graph(all_entities, all_relations)
                    all_entities = []
                    all_relations = []
            
            # Add remaining entities and relations
            if all_entities or all_relations:
                self.add_to_graph(all_entities, all_relations)
            
            # Get final stats
            stats = self.get_graph_stats()
            logger.info(f"✅ Knowledge graph built: {stats['num_nodes']} entities, {stats['num_relationships']} relations")
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            # Don't raise - allow RAG to continue working
            logger.warning("⚠️ KG processing failed, but RAG will still work")
    
    def query_graph(self, question: str, limit: int = 10) -> Dict[str, Any]:
        """Query the knowledge graph"""
        try:
            # Extract key entities from question
            doc = self.nlp(question)
            query_entities = [ent.text for ent in doc.ents]
            
            if not query_entities:
                # Use noun chunks if no entities found
                query_entities = [chunk.text for chunk in doc.noun_chunks][:3]
            
            results = {
                "entities": [],
                "relations": [],
                "answer": ""
            }
            
            with self.driver.session() as session:
                # Find related entities and relationships
                for entity in query_entities:
                    # Get entity and its relationships
                    result = session.run(
                        """
                        MATCH (e:Entity)
                        WHERE toLower(e.name) CONTAINS toLower($entity)
                        OPTIONAL MATCH (e)-[r]->(related)
                        RETURN e.name as entity, e.type as type, 
                               type(r) as relation, related.name as related_entity
                        LIMIT $limit
                        """,
                        entity=entity,
                        limit=limit
                    )
                    
                    for record in result:
                        if record["entity"]:
                            results["entities"].append(record["entity"])
                        
                        if record["relation"] and record["related_entity"]:
                            relation_text = f"{record['entity']} -> {record['relation']} -> {record['related_entity']}"
                            results["relations"].append(relation_text)
            
            # Generate answer from graph results
            if results["entities"] or results["relations"]:
                results["answer"] = self._generate_answer_from_graph(question, results)
            else:
                results["answer"] = "No relevant information found in the knowledge graph."
            
            return results
            
        except Exception as e:
            logger.error(f"Graph query failed: {e}")
            return {
                "entities": [],
                "relations": [],
                "answer": f"Query failed: {str(e)}"
            }
    
    def _generate_answer_from_graph(self, question: str, graph_results: Dict) -> str:
        """Generate natural language answer from graph results"""
        try:
            context = f"""
            Question: {question}
            
            Related Entities: {', '.join(graph_results['entities'][:10])}
            
            Relationships: {chr(10).join(graph_results['relations'][:5])}
            """
            
            prompt = PromptTemplate(
                input_variables=["context"],
                template="""
                Based on the following knowledge graph information, provide a concise answer:
                
                {context}
                
                Answer:
                """
            )
            
            response = self.llm.invoke(prompt.format(context=context))
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return answer.strip()
            
        except Exception as e:
            logger.error(f"Answer generation failed: {e}")
            return "Unable to generate answer from knowledge graph."
    
    def get_graph_stats(self) -> Dict[str, int]:
        """Get statistics about the knowledge graph"""
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (n)
                    OPTIONAL MATCH ()-[r]->()
                    RETURN count(DISTINCT n) as num_nodes, count(r) as num_relationships
                    """
                )
                
                record = result.single()
                return {
                    "num_nodes": record["num_nodes"],
                    "num_relationships": record["num_relationships"]
                }
                
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {"num_nodes": 0, "num_relationships": 0}
    
    def clear_graph(self):
        """Clear all data from the knowledge graph"""
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
            logger.info("Knowledge graph cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear graph: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection"""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.close()
                logger.info("Neo4j connection closed")
        except Exception as e:
            logger.error(f"Error closing Neo4j connection: {e}")

    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.close()
        except:
            pass