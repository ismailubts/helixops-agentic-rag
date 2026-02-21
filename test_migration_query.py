import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from state import AgentState
from nodes import retrieve, grade_documents, generate, web_search


def create_rag_graph() -> StateGraph:
    """Create the Agentic RAG StateGraph with self-correction loop."""
    
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
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
    """Test the 2026 Gemini migration efficiency query."""
    # Load environment variables
    load_dotenv()
    
    # Create the graph
    app = create_rag_graph()
    
    print("Testing 2026 Gemini Migration Efficiency Query")
    print("=" * 50)
    
    # Test the specific query about 2026 migration efficiency
    query = "What is the primary efficiency gain of 2026 Gemini migration?"
    
    print(f"Query: {query}")
    print("-" * 50)
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "documents": [],
        "is_relevant": False,
        "web_search_performed": False
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Print results
    print(f"Documents retrieved: {len(result['documents'])}")
    print(f"Documents relevant: {result['is_relevant']}")
    
    # Print final answer
    print("\nFinal Answer:")
    print("-" * 20)
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            print(message.content)
    
    # Check for 25% latency reduction
    final_answer = ""
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            final_answer = message.content.lower()
    
    if "25%" in final_answer and "latency" in final_answer:
        print("\n✅ SUCCESS: Answer correctly mentions 25% latency reduction!")
    elif "25%" in final_answer:
        print("\n⚠️  PARTIAL: Answer mentions 25% but not specifically latency reduction")
    else:
        print("\n❌ ISSUE: Answer does not mention 25% latency reduction")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
