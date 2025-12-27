# Technical Report: Multi-Agent AI Customer Support System with n8n
*by Zakaria Chaara*
## 1. System Overview

This system automates customer support using multiple AI agents that work together to understand customer questions, analyze their emotions, provide answers, and create support tickets when needed. The system runs entirely on local infrastructure, ensuring data privacy and cost efficiency.

## 2. AI Agents and Their Roles

The system consists of eight specialized AI agents:

### 2.1 Core Processing Agents

**Intent Classifier Agent**
- Reads customer messages
- Identifies what the customer needs (order status, refund, technical help, general questions, or escalation)
- Routes the conversation to the right specialist agent

**Sentiment Analyzer Agent** 
- Analyzes customer emotions (positive, negative, or neutral)
- Flags negative sentiment for priority handling
- Helps identify frustrated customers who need immediate attention

### 2.2 Specialist Response Agents

**Order Support Agent**
- Handles order tracking questions
- Retrieves order status from the database
- Provides delivery estimates and tracking numbers

**Refund Agent**
- Processes refund requests
- Explains refund policies (30-day window, unused products)
- Guides customers through the refund process

**Product Issue Agent**
- Troubleshoots technical problems
- Asks diagnostic questions
- Provides step-by-step solutions

**FAQ Agent**
- Answers general questions (business hours, shipping times, contact information)
- Provides company policy information
- Handles simple inquiries

**Escalation Agent**
- Handles complex or sensitive issues
- Creates support tickets for human agents
- Prioritizes tickets based on sentiment analysis

**Memory Agent**
- Stores conversation summaries in the database
- Retrieves past interactions with the customer
- Enables personalized responses based on customer history

## 3. How Agents Work Together

### 3.1 Workflow Structure

The agents follow this sequence when processing customer requests:

```
Customer Message
    ↓
[1] Intent Classifier determines the request type
    ↓
[2] Sentiment Analyzer checks customer emotions
    ↓
[3] Memory Agent retrieves past conversations
    ↓
[4] Decision Point: Is sentiment negative?
    ├─ YES → Flag for escalation → Route to Escalation Agent
    └─ NO → Route to appropriate specialist agent
    ↓
[5] Specialist Agent (Order/Refund/Product/FAQ/Escalation) processes request
    ↓
[6] If escalated: Create Support Ticket tool is called
    ↓
[7] Response is formatted with sentiment and ticket ID
    ↓
[8] Memory Agent summarizes and stores conversation
    ↓
Reply sent to customer
```

### 3.2 Agent Communication

Agents communicate through n8n workflow nodes:

- **Sequential Processing**: Each agent passes its output to the next agent in line
- **Conditional Routing**: Switch nodes direct conversations based on intent and sentiment
- **Parallel Memory Operations**: Memory retrieval happens early; memory storage happens at the end
- **Tool Integration**: Agents call external tools (order database, ticket system) when needed

## 4. Key Technical Features

### 4.1 Sentiment-Based Escalation
- **Purpose**: Automatically identify unhappy customers before issues worsen
- **Implementation**: Negative sentiment triggers immediate escalation regardless of intent
- **Benefit**: Reduces customer churn by providing faster attention to frustrated users

### 4.2 Support Ticket Creation
- **Purpose**: Create formal records for human agents when AI cannot resolve issues
- **Implementation**: REST API tool that generates unique ticket IDs and stores issue details
- **Benefit**: Ensures seamless handoff from AI to human support with complete context

### 4.3 Conversation Summarization
- **Purpose**: Store conversation history efficiently for long-term memory
- **Implementation**: AI summarizes each conversation into one concise sentence (max 20 words)
- **Example**: Instead of storing 200 words, system stores: "Customer inquired about refund policy for damaged item"
- **Benefit**: Reduces storage costs by 80-90% while maintaining context

### 4.4 Context-Aware Responses
- **Purpose**: Personalize responses based on customer history
- **Implementation**: Before answering, agents retrieve and review past interactions
- **Benefit**: Customers don't need to repeat information; agents recognize returning customers

## 5. System Architecture

### 5.1 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| User Interface | Streamlit | Customer chat interface |
| Orchestration | n8n | Agent coordination and workflow |
| AI Model | Ollama (LLaMA 3.1 8B) | Natural language understanding |
| Memory Database | ChromaDB | Vector-based conversation storage |
| Tool Server | FastAPI | Order lookup and ticket creation |
| Communication | REST APIs | Data exchange between components |

### 5.2 Data Flow

```
Customer types message in Streamlit
    ↓
Message sent to n8n webhook (POST request)
    ↓
n8n orchestrates 8 agents sequentially
    ↓
Agents call Ollama for language processing
    ↓
Tools retrieve data from databases
    ↓
Memory stores conversation summary
    ↓
Response sent back to Streamlit
    ↓
Customer sees reply with sentiment and ticket info
```

## 6. Conclusion

This multi-agent system demonstrates how AI can automate customer support while maintaining quality and empathy. The integration of sentiment analysis ensures emotional intelligence, support ticket creation enables smooth AI-to-human handoffs, and conversation summarization makes the system scalable and cost-effective.

The modular architecture allows easy addition of new agents or tools. The system runs entirely on local infrastructure, ensuring data privacy and eliminating API costs. This design provides a practical template for deploying intelligent automation in real-world business environments.

## 7. Technical Implementation Summary

**Total Components**: 8 AI agents + 3 tool servers + 1 vector database
**Programming Languages**: Python (tools/GUI), JavaScript (workflow logic)
**External Dependencies**: Ollama, n8n, ChromaDB, FastAPI, Streamlit
**Deployment Model**: Fully local 
