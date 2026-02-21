import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from state import AgentState
from nodes import retrieve, grade_documents_mock, generate_mock, web_search


def create_rag_graph() -> StateGraph:
    """Create the Agentic RAG StateGraph with self-correction loop."""
    
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents_mock)
    workflow.add_node("generate", generate_mock)
    workflow.add_node("web_search", web_search)
    
    # Add edges
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    
    # Conditional edge for self-correction loop
    def decide_next_step(state: AgentState) -> str:
        """Determine next step based on document relevance."""
        
        # If web search was already performed, go to generation to prevent infinite loop
        if state.get("web_search_performed", False):
            return "generate"
        
        if state.get("is_relevant", False):
            return "generate"
        else:
            return "web_search"
    
    workflow.add_conditional_edges(
        "grade_documents",
        decide_next_step,
        {
            "generate": "generate",
            "web_search": "web_search"
        }
    )
    
    # Complete the loop
    workflow.add_edge("web_search", "retrieve")
    workflow.add_edge("generate", END)
    
    return workflow.compile()


def main():
    """Test the self-correction loop with different queries."""
    # Load environment variables
    load_dotenv()
    
    # Create the graph
    app = create_rag_graph()
    
    # Test queries
    test_queries = [
        {
            "query": "Tell me about TechFlow AI's RAG architecture",
            "expected_relevant": True,
            "description": "Relevant query about TechFlow AI"
        },
        {
            "query": "What is the weather like on Mars?",
            "expected_relevant": False,
            "description": "Irrelevant query - should trigger self-correction"
        },
        {
            "query": "How do I bake a chocolate cake?",
            "expected_relevant": False,
            "description": "Another irrelevant query - should trigger web search"
        }
    ]
    
    print("Testing Agentic RAG System Self-Correction Loop")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n--- Test Case {i}: {test_case['description']} ---")
        print(f"Query: {test_case['query']}")
        
        # Initial state with a user question
        initial_state = {
            "messages": [HumanMessage(content=test_case['query'])],
            "documents": [],
            "is_relevant": False,
            "web_search_performed": False
        }
        
        # Run the graph
        result = app.invoke(initial_state, config={"recursion_limit": 50})
        
        # Print results
        print(f"Documents retrieved: {len(result['documents'])}")
        print(f"Documents relevant: {result['is_relevant']}")
        print(f"Expected relevant: {test_case['expected_relevant']}")
        
        # Check if self-correction was triggered
        ai_messages = [msg for msg in result['messages'] if isinstance(msg, AIMessage)]
        if len(ai_messages) > 1:
            print("✅ Self-correction loop triggered (multiple AI messages)")
        elif len(ai_messages) == 1:
            print("✅ Direct generation (no self-correction needed)")
        
        # Print final answer
        print("\nFinal Answer:")
        print("-" * 20)
        for message in ai_messages:
            print(message.content)
        
        print("=" * 60)


if __name__ == "__main__":
    main()
