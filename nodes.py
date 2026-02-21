from typing import List
import json
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import AgentState


def retrieve(state: AgentState) -> AgentState:
    """Retrieve documents from ChromaDB based on the query."""
    # Load ChromaDB JSON files
    try:
        with open("./chroma_db/documents.json", "r", encoding="utf-8") as f:
            documents = json.load(f)
    except FileNotFoundError:
        state["documents"] = []
        return state
    
    # Get the latest human message as query
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages:
        return state
    
    query = human_messages[-1].content
    
    # Simple keyword matching for retrieval
    relevant_docs = []
    query_keywords = query.lower().split()
    
    for doc in documents:
        doc_content = doc["content"].lower()
        # Check if any query keywords are in document
        if any(keyword in doc_content for keyword in query_keywords if len(keyword) > 2):
            relevant_docs.append(doc["content"])
    
    # Limit to top 4 documents
    state["documents"] = relevant_docs[:4]
    
    return state


def grade_documents(state: AgentState) -> AgentState:
    """Grade documents for relevance using LLM."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Get the latest human message and documents
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages or not state["documents"]:
        state["is_relevant"] = False
        return state
    
    query = human_messages[-1].content
    documents_text = "\n\n".join(state["documents"])
    
    # Grade the documents
    grading_prompt = f"""
    You are an expert at determining document relevance for RAG systems.
    
    Query: {query}
    
    Documents:
    {documents_text}
    
    Analyze the documents and determine if they are relevant to answering the query.
    Consider:
    1. Do the documents contain information that directly addresses the query?
    2. Are the documents sufficiently detailed to provide a comprehensive answer?
    3. Is the information up-to-date and accurate?
    
    Respond with only "RELEVANT" or "IRRELEVANT".
    """
    
    response = llm.invoke(grading_prompt)
    state["is_relevant"] = "RELEVANT" in response.content.upper()
    
    return state


def generate(state: AgentState) -> AgentState:
    """Generate RAG answer using retrieved documents."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    # Get the latest human message and documents
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages:
        return state
    
    query = human_messages[-1].content
    
    if state["documents"]:
        documents_text = "\n\n".join(state["documents"])
        context_prompt = f"""
        You are a helpful AI assistant. Use the following retrieved documents to answer the user's question.
        If the documents don't contain enough information, say so clearly.
        
        Question: {query}
        
        Retrieved Documents:
        {documents_text}
        
        Provide a comprehensive answer based on the retrieved documents:
        """
    else:
        context_prompt = f"""
        You are a helpful AI assistant. Answer the following question to the best of your ability.
        
        Question: {query}
        
        Since no relevant documents were found, provide a general response:
        """
    
    response = llm.invoke(context_prompt)
    
    # Add the AI response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state


def web_search(state: AgentState) -> AgentState:
    """Placeholder for web search functionality."""
    # This is a placeholder for web search implementation
    # In a real implementation, you would use a web search API here
    
    # Add a message indicating web search was performed
    state["messages"].append(
        AIMessage(content="Web search was performed to find additional relevant information.")
    )
    
    # Clear documents to trigger re-retrieval
    state["documents"] = []
    
    # Mark as relevant and set flag to prevent infinite loop
    state["is_relevant"] = True
    state["web_search_performed"] = True
    
    return state


def grade_documents_mock(state: AgentState) -> AgentState:
    """Mock version of grade_documents that doesn't require API calls."""
    # Get the latest human message and documents
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages or not state["documents"]:
        state["is_relevant"] = False
        return state
    
    query = human_messages[-1].content.lower()
    documents_text = " ".join(state["documents"]).lower()
    
    # TechFlow AI relevant keywords
    techflow_keywords = ["techflow", "rag", "architecture", "deployment", "algorithm", "system", "enterprise", "solution"]
    
    # Check if query contains TechFlow AI related terms
    query_has_techflow_terms = any(keyword in query for keyword in techflow_keywords)
    
    # Check if documents contain relevant information
    docs_have_techflow_info = any(keyword in documents_text for keyword in techflow_keywords)
    
    # Documents are relevant only if both query and documents are about TechFlow AI
    state["is_relevant"] = query_has_techflow_terms and docs_have_techflow_info
    
    return state


def generate_mock(state: AgentState) -> AgentState:
    """Mock version of generate that doesn't require API calls."""
    # Get the latest human message and documents
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages:
        return state
    
    query = human_messages[-1].content
    
    if state["documents"] and state["is_relevant"]:
        # Generate a mock response based on the query and documents
        if "architecture" in query.lower():
            response = """
            Based on the retrieved documents, TechFlow AI's RAG architecture includes:
            
            Core Components:
            - Vector Database: ChromaDB for efficient similarity search
            - Document Processing: Automated chunking and embedding
            - LLM Integration: OpenAI GPT models for generation
            - Self-Correction Loop: Automatic relevance checking and fallback mechanisms
            
            The system implements a sophisticated self-correction mechanism that ensures 
            high-quality responses through intelligent document relevance assessment.
            """
        elif "deployment" in query.lower():
            response = """
            TechFlow AI offers flexible deployment solutions:
            
            Cloud-Based Solution:
            - Managed infrastructure with 99.9% uptime
            - Automatic scaling based on query volume
            - Integrated monitoring and alerting
            - SOC 2 Type II compliance
            
            On-Premises Deployment:
            - Complete data sovereignty
            - Custom integration with existing systems
            - Dedicated support team
            
            Hybrid Architecture:
            - Cloud-based processing with on-premises data storage
            - Best of both worlds for regulated industries
            """
        elif "algorithm" in query.lower() or "self-correction" in query.lower():
            response = """
            TechFlow AI's Self-Correction Algorithm:
            
            Steps:
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
            """
        else:
            response = f"""
            Based on the retrieved documents about TechFlow AI, I found relevant information 
            regarding your query about "{query}". The documents cover various aspects of 
            TechFlow AI's enterprise RAG solutions, including technical specifications, 
            deployment options, and customer success stories.
            """
    else:
        response = f"""
        I couldn't find relevant information about "{query}" in the current document database. 
        The available documents focus on TechFlow AI's RAG architecture and enterprise solutions. 
        For more specific information, you might want to try a different query or consult 
        the official TechFlow AI documentation.
        """
    
    # Add the AI response to messages
    state["messages"].append(AIMessage(content=response))
    
    return state
