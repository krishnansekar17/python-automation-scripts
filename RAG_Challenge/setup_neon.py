import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Get connection details from .env
NEON_DB_HOST = os.getenv("NEON_DB_HOST")
NEON_DB_NAME = os.getenv("NEON_DB_NAME")
NEON_DB_USER = os.getenv("NEON_DB_USER")
NEON_DB_PASSWORD = os.getenv("NEON_DB_PASSWORD")
NEON_DB_PORT = os.getenv("NEON_DB_PORT", "5432")

# Create connection string
connection_string = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}?sslmode=require"

print("🔌 Connecting to Neon Postgres...")
print(f"Host: {NEON_DB_HOST}")

try:
    # Connect to database
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    
    print("✅ Connected successfully!")
    
    # Enable pgvector extension
    print("📦 Installing pgvector extension...")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    
    print("✅ pgvector extension enabled!")
    
    # Verify installation
    cursor.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")
    result = cursor.fetchone()
    
    if result:
        print(f"✅ Verification successful: {result[0]} version {result[1]}")
    else:
        print("⚠️ Warning: Could not verify pgvector installation")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n🎉 Neon Postgres setup complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check your .env file has correct credentials")
    print("2. Verify your Neon project is active")
    print("3. Check your internet connection")