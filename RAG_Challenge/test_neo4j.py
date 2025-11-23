from neo4j import GraphDatabase

uri = "bolt://localhost:7689"
username = "neo4j"
password = "testpassword123"

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' AS message")
        message = result.single()["message"]
        print(f"✅ {message}")
    driver.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")