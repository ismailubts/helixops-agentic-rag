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
    """Main function to run the Agentic RAG system."""
    # Load environment variables
    load_dotenv()
    
    # Create the graph
    app = create_rag_graph()
    
    # Example usage
    print("Agentic RAG System with Self-Correction Loop")
    print("=" * 50)
    
    # Initial state with a user question
    initial_state = {
        "messages": [
            HumanMessage(content="Tell me about TechFlow AI's RAG architecture")
        ],
        "documents": [],
        "is_relevant": False,
        "web_search_performed": False
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Print the final answer
    print("\nFinal Answer:")
    print("-" * 20)
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            print(message.content)
    
    print(f"\nDocuments retrieved: {len(result['documents'])}")
    print(f"Documents relevant: {result['is_relevant']}")


if __name__ == "__main__":
    main()
