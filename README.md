# Agentic RAG System with Self-Correction Loop

A professional-grade Retrieval-Augmented Generation (RAG) system built with LangGraph and LangChain v0.3, featuring an intelligent self-correction mechanism.

## 🚀 Key Features

### Self-Correction Loop
The standout technical feature of this system is its **self-correction loop** that automatically handles irrelevant retrieved documents:

1. **Document Retrieval**: Fetches relevant documents from ChromaDB
2. **Relevance Grading**: Uses LLM to evaluate if retrieved documents are relevant to the query
3. **Conditional Routing**: 
   - ✅ If documents are relevant → Proceed to answer generation
   - ❌ If documents are irrelevant → Trigger web search and re-retrieve
4. **Web Search Fallback**: Placeholder for web search to find additional relevant information
5. **Loop Continuation**: System automatically retries retrieval until relevant documents are found

This creates a resilient RAG system that doesn't fail when initial document retrieval yields poor results.

## 📁 Project Structure

```
ai-agent-project/
├── requirements.txt          # Dependencies
├── state.py                 # Agent state definition
├── nodes.py                 # RAG node implementations
├── main.py                  # Graph compilation and execution
└── README.md               # Documentation
```

## 🛠️ Technology Stack

- **LangChain v0.3**: Core RAG framework
- **LangGraph**: Agent orchestration and state management
- **ChromaDB**: Vector database for document storage
- **OpenAI**: Embeddings and LLM models
- **Python 3.9+**: Runtime environment

## 📋 Components

### State Management (`state.py`)
- `AgentState`: TypedDict defining agent state with:
  - `messages`: Conversation history with `add_messages` annotation
  - `documents`: Retrieved document contents
  - `is_relevant`: Boolean flag for document relevance

### Node Logic (`nodes.py`)
- **retrieve**: ChromaDB similarity search
- **grade_documents**: LLM-based relevance assessment
- **generate**: RAG answer generation
- **web_search**: Placeholder for web search fallback

### Graph Compilation (`main.py`)
- Modern LangGraph patterns with START/END nodes
- Conditional edge implementation for self-correction
- Complete workflow orchestration

## 🚦 Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the system:
```bash
python main.py
```

## 🔄 Self-Correction Flow

```
START → retrieve → grade_documents
                     ↓
        is_relevant? → generate → END
                     ↓
              web_search → retrieve (loop)
```

## 🎯 Use Cases

- **Question Answering**: Robust QA system with fallback mechanisms
- **Research Assistant**: Automated document retrieval with quality assurance
- **Customer Support**: Intelligent response generation with verification
- **Knowledge Management**: Reliable information extraction from document stores

## 🔧 Configuration

The system uses modern LangGraph patterns:
- `add_messages` annotation for automatic message history management
- START/END nodes for clear workflow boundaries
- Conditional edges for intelligent routing
- TypedDict state for type safety

## 🚀 Extending the System

- Implement actual web search in the `web_search` node
- Add more sophisticated grading criteria
- Integrate with different vector databases
- Add caching mechanisms for repeated queries
- Implement multi-turn conversations with context preservation

## 📊 Performance Considerations

- The self-correction loop may increase latency but improves accuracy
- Consider implementing relevance thresholds to prevent infinite loops
- Monitor LLM costs for document grading
- Optimize ChromaDB indexes for faster retrieval
