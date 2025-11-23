"""
Configuration management for the Hybrid RAG + KG Assistant
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for application settings"""
    
    def __init__(self):
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
        # Neon Postgres Configuration
        self.NEON_DB_HOST = os.getenv("NEON_DB_HOST")
        self.NEON_DB_NAME = os.getenv("NEON_DB_NAME", "neondb")
        self.NEON_DB_USER = os.getenv("NEON_DB_USER")
        self.NEON_DB_PASSWORD = os.getenv("NEON_DB_PASSWORD")
        self.NEON_DB_PORT = os.getenv("NEON_DB_PORT", "5432")
        
        # Neo4j Configuration
        self.NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
        
        # RAG Configuration
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
        self.TOP_K = int(os.getenv("TOP_K", "5"))
        
        # Paths
        self.BASE_DIR = Path(__file__).parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.UPLOAD_DIR = self.DATA_DIR / "uploads"
        
        # Create directories if they don't exist
        self.DATA_DIR.mkdir(exist_ok=True)
        self.UPLOAD_DIR.mkdir(exist_ok=True)
    
    @property
    def neo4j_uri(self):
        """Get Neo4j URI"""
        return self.NEO4J_URI
    
    @property
    def neon_connection_string(self):
        """Generate Neon Postgres connection string with SSL and keepalive parameters"""
        if not all([self.NEON_DB_HOST, self.NEON_DB_USER, self.NEON_DB_PASSWORD]):
            raise ValueError("Neon database credentials not configured")
        
        # Build connection string with SSL and connection pooling parameters
        conn_str = (
            f"postgresql://{self.NEON_DB_USER}:{self.NEON_DB_PASSWORD}"
            f"@{self.NEON_DB_HOST}:{self.NEON_DB_PORT}/{self.NEON_DB_NAME}"
            f"?sslmode=require"
            f"&connect_timeout=10"
            f"&keepalives=1"
            f"&keepalives_idle=30"
            f"&keepalives_interval=10"
            f"&keepalives_count=5"
            f"&application_name=hybrid-rag-assistant"
        )
        
        return conn_str
    
    def validate(self):
        """Validate configuration"""
        required_vars = [
            ("OPENAI_API_KEY", self.OPENAI_API_KEY),
            ("NEON_DB_HOST", self.NEON_DB_HOST),
            ("NEON_DB_USER", self.NEON_DB_USER),
            ("NEON_DB_PASSWORD", self.NEON_DB_PASSWORD),
            ("NEO4J_URI", self.NEO4J_URI),
            ("NEO4J_USER", self.NEO4J_USER),
            ("NEO4J_PASSWORD", self.NEO4J_PASSWORD),
        ]
        
        missing = [name for name, value in required_vars if not value]
        
        if missing:
            print(f"❌ Missing configuration: {', '.join(missing)}")
            return False
        
        print("✅ Configuration valid")
        return True

# Create global config instance
config = Config()