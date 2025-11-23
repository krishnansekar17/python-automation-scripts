from langchain_openai import OpenAIEmbeddings
from config.config import config

try:
    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY
    )
    
    test_text = "This is a test"
    result = embeddings.embed_query(test_text)
    
    print(f"✅ Embeddings working! Vector dimension: {len(result)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()