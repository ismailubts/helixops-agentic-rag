import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def seed_mock_db():
    """Create a mock vector database for testing without ChromaDB."""
    
    # Create mock database directory
    os.makedirs("./mock_db", exist_ok=True)
    
    # TechFlow AI corporate documents
    documents = [
        {
            "id": "techflow_overview",
            "content": """
            TechFlow AI: Enterprise RAG Architecture Overview
            
            TechFlow AI is a leading provider of enterprise-grade Retrieval-Augmented Generation (RAG) solutions. 
            Our architecture leverages advanced vector databases, large language models, and intelligent document 
            processing pipelines to deliver accurate, context-aware responses for enterprise applications.
            
            Key Components:
            - Vector Database: ChromaDB for efficient similarity search
            - Document Processing: Automated chunking and embedding
            - LLM Integration: OpenAI GPT models for generation
            - Self-Correction Loop: Automatic relevance checking and fallback mechanisms
            """,
            "metadata": {"source": "corporate_overview", "company": "TechFlow AI"}
        },
        {
            "id": "techflow_specs",
            "content": """
            TechFlow AI RAG System Technical Specifications
            
            Our RAG system implements a sophisticated self-correction mechanism that ensures high-quality 
            responses through intelligent document relevance assessment.
            
            Technical Stack:
            - LangChain v0.3: Core framework for RAG operations
            - LangGraph: Agent orchestration with conditional routing
            - ChromaDB: Persistent vector storage with metadata filtering
            - OpenAI Embeddings: Text-to-vector conversion
            - GPT-4o-mini: Efficient generation and document grading
            
            Performance Metrics:
            - Retrieval Latency: <200ms for typical queries
            - Relevance Accuracy: 94% with self-correction loop
            - Document Processing: 1000+ documents per minute
            """,
            "metadata": {"source": "technical_specs", "company": "TechFlow AI"}
        },
        {
            "id": "techflow_algorithm",
            "content": """
            TechFlow AI Self-Correction Algorithm
            
            The self-correction loop is our patented approach to handling irrelevant or insufficient retrieved documents.
            
            Algorithm Steps:
            1. Initial document retrieval from vector database
            2. LLM-based relevance assessment using structured prompts
            3. Conditional routing based on relevance score
            4. Web search fallback for irrelevant results
            5. Re-retrieval with expanded query parameters
            6. Final generation with verified relevant documents
            
            Benefits:
            - Eliminates hallucination from poor context
            - Improves answer accuracy by 40%
            - Reduces user frustration with irrelevant responses
            - Adapts to domain-specific terminology
            """,
            "metadata": {"source": "algorithm_details", "company": "TechFlow AI"}
        },
        {
            "id": "techflow_deployment",
            "content": """
            TechFlow AI Enterprise Deployment Options
            
            We offer flexible deployment solutions tailored to enterprise needs:
            
            Cloud-Based Solution:
            - Managed infrastructure with 99.9% uptime
            - Automatic scaling based on query volume
            - Integrated monitoring and alerting
            - SOC 2 Type II compliance
            
            On-Premises Deployment:
            - Complete data sovereignty
            - Custom integration with existing systems
            - Dedicated support team
            - One-time licensing option
            
            Hybrid Architecture:
            - Cloud-based processing with on-premises data storage
            - Best of both worlds for regulated industries
            - Seamless migration path
            - Cost optimization through intelligent routing
            """,
            "metadata": {"source": "deployment_options", "company": "TechFlow AI"}
        },
        {
            "id": "techflow_cases",
            "content": """
            TechFlow AI Customer Success Stories
            
            Global Financial Services Firm:
            - Challenge: Processing 50,000+ financial documents for customer service
            - Solution: Custom RAG system with domain-specific embeddings
            - Results: 60% reduction in response time, 85% customer satisfaction
            
            Healthcare Provider Network:
            - Challenge: Accurate medical information retrieval across 200+ facilities
            - Solution: HIPAA-compliant RAG with enhanced privacy controls
            - Results: 45% faster diagnosis support, zero privacy breaches
            
            Manufacturing Enterprise:
            - Challenge: Technical documentation access for 10,000+ engineers
            - Solution: Multi-language RAG with technical terminology optimization
            - Results: 70% reduction in support tickets, 92% engineer adoption rate
            """,
            "metadata": {"source": "case_studies", "company": "TechFlow AI"}
        }
    ]
    
    # Save documents to JSON file
    with open("./mock_db/documents.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created mock database with {len(documents)} TechFlow AI documents")
    print("Database saved to ./mock_db/documents.json")
    
    # Test the database
    print("\nTesting mock database with sample query...")
    query = "TechFlow AI RAG architecture"
    
    # Simple keyword matching for mock retrieval
    relevant_docs = []
    for doc in documents:
        if any(keyword.lower() in doc["content"].lower() for keyword in query.split()):
            relevant_docs.append(doc)
    
    print(f"Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs[:2], 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc['metadata'].get('source', 'unknown')}")
        print(f"Content: {doc['content'][:200]}...")

if __name__ == "__main__":
    seed_mock_db()
