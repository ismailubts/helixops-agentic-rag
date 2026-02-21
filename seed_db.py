import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def seed_chroma_db():
    """Initialize mock database with TechFlow AI corporate documents (compatible version)."""
    
    # Create mock database directory
    os.makedirs("./chroma_db", exist_ok=True)
    
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
            - LLM Integration: Gemini 2.5 Flash for generation
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
            - Google Native Embeddings: Text-to-vector conversion
            - Gemini 2.5 Flash: Efficient generation and document grading
            
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
            "id": "techflow_migration_2026",
            "content": """
            TechFlow AI 2026 Gemini Migration Performance Update
            
            The 2026 migration to Gemini-native architecture represents a significant leap in RAG system performance 
            and operational efficiency. This comprehensive migration focused on leveraging Google's advanced AI 
            infrastructure while maintaining our patented self-correction mechanisms.
            
            Key Migration Benefits:
            - 25% reduction in overall system latency across all query types
            - Improved cross-node orchestration through Gemini's native graph processing
            - Enhanced token efficiency reducing operational costs by 30%
            - Native integration with Google's vector embedding services
            - Zero-downtime migration maintaining 99.9% service availability
            
            Technical Improvements:
            - Gemini 2.5 Flash: 40% faster response generation compared to previous models
            - Google Native Embeddings: 35% improvement in semantic similarity accuracy
            - Optimized LangGraph conditional routing with Gemini's enhanced reasoning
            - Enhanced self-correction loop with improved relevance assessment
            
            Performance Metrics Post-Migration:
            - End-to-end latency: Reduced from 450ms to 337ms (25% improvement)
            - Query throughput: Increased by 45% with Gemini's parallel processing
            - Relevance accuracy: Improved from 94% to 96.5%
            - System reliability: Maintained 99.9% uptime with enhanced error recovery
            
            The migration ensures TechFlow AI remains at the forefront of enterprise RAG solutions 
            while delivering measurable performance improvements to our global customer base.
            """,
            "metadata": {"source": "migration_update", "company": "TechFlow AI"}
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
    
    # Save documents to JSON file (ChromaDB-compatible format)
    with open("./chroma_db/documents.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    # Create metadata file for ChromaDB simulation
    metadata = {
        "collection_name": "techflow_documents",
        "embedding_function": "google_native",
        "total_documents": len(documents),
        "created_at": "2026-02-21",
        "migration_status": "gemini_25_native"
    }
    
    with open("./chroma_db/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Successfully seeded ChromaDB with {len(documents)} TechFlow AI documents")
    print("Database saved to ./chroma_db directory")
    
    # Test the database
    print("\nTesting database with sample query...")
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
    seed_chroma_db()
