import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import OllamaLLM
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic.prompts import PromptTemplate
import time

async def setup_agent():
    print("🔗 Setting up MCP connections (async)...")
    
    # 1. Setup MultiServerMCPClient with CORRECT configuration
    try:
        # Create connections dictionary with TRANSPORT key (required!)
        connections = {
            "budget": {
                "transport": "sse",  # ← REQUIRED KEY
                "url": "http://localhost:3333/sse"
            },
            "destination": {
                "transport": "sse",
                "url": "http://localhost:3334/sse"
            },
            "weather": {
                "transport": "sse", 
                "url": "http://localhost:3335/sse"
            },
            "currency": {
                "transport": "sse",
                "url": "http://localhost:3336/sse"
            },
            "calculator": {
                "transport": "sse",
                "url": "http://localhost:3337/sse"
            }
        }
        
        print(f"✅ Configuring {len(connections)} connections with transport='sse'")
        
        # Create client
        client = MultiServerMCPClient(connections=connections)
        print("✅ MultiServerMCPClient created")
        
        # Get tools ASYNC
        tools = await client.get_tools()
        print(f"📊 Successfully loaded {len(tools)} tools")
        
        # List all tools
        for i, tool in enumerate(tools):
            print(f"  {i+1}. {tool.name}: {tool.description[:60]}...")
            
    except Exception as e:
        print(f"❌ MCP setup failed: {e}")
        
        # Fallback to mock tools
        from langchain.tools import Tool
        tools = []
        
        mock_config = [
            ("budget_calculator", "Calculate travel budget"),
            ("destination_finder", "Find travel destinations"),
            ("weather_checker", "Check weather forecast"),
            ("currency_converter", "Convert currencies"),
            ("basic_calculator", "Perform calculations")
        ]
        
        for name, desc in mock_config:
            def create_func(tool_name, tool_desc):
                return lambda **kwargs: f"[{tool_name}] Called with: {kwargs}"
            
            tools.append(Tool(
                name=name,
                func=create_func(name, desc),
                description=desc
            ))
        
        print(f"⚠️  Using {len(tools)} mock tools")
    
    # 2. Initialize Ollama
    print("\n🚀 Initializing Ollama...")
    try:
        llm = OllamaLLM(
            model="llama3.2:1b",
            temperature=0.1,
            num_predict=512,
        )
        print("🤖 Ollama initialized")
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        from langchain_community.llms import Ollama
        llm = Ollama(model="llama3.2:1b", temperature=0.1)
    
    # 3. Create agent with CORRECT prompt template
    if tools and llm:
        try:
        # CORRECT PromptTemplate with ALL required variables
            prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
                template="""
You are a helpful travel planning assistant with access to these tools:

{tools}

Use this format:
Thought: [your reasoning]
Action: [{tool_names}]
Action Input: [tool input]
Observation: [tool result]

Question: {input}
Thought: {agent_scratchpad}
"""
            )
            
            print("📝 Creating agent with prompt template...")
            
            # Create agent
            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt
            )
            
            # Create executor
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True
            )
            
            print("✅ Agent setup complete!")
            return agent_executor
            
        except Exception as e:
            print(f"❌ Agent creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    else:
        print("❌ Missing tools or LLM")
        return None

# Run async setup
print("=" * 50)
print("Starting agent setup...")
print("=" * 50)

agent_executor = asyncio.run(setup_agent())

# Sync wrapper function
def run_travel_agent(user_request: str):
    """Run the travel planning agent"""
    if not agent_executor:
        return "Agent not initialized"
    
    try:
        print(f"\n📝 Processing: {user_request}")
        print("-" * 40)
        start_time = time.time()
        
        result = agent_executor.invoke({"input": user_request})
        
        elapsed = time.time() - start_time
        print(f"\n⏱️  Response time: {elapsed:.2f}s")
        return result.get("output", str(result))
        
    except Exception as e:
        return f"Error: {str(e)}"

