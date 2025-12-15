import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import OllamaLLM
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic.prompts import PromptTemplate
import time
from langchain_classic.tools import Tool
import json

# Global storage for tool calls
TOOL_CALLS_HISTORY = []

def track_tool_call(tool_name, tool_input, tool_output):
    """Simple function to track tool calls"""
    call_data = {
        'tool': tool_name,
        'input': tool_input,
        'output': str(tool_output)[:1000],  # Limit output length
        'timestamp': time.time()
    }
    TOOL_CALLS_HISTORY.append(call_data)
    print(f"🔧 Tool used: {tool_name} with input: {tool_input}")
    return call_data

def get_tool_calls():
    """Get all tool calls"""
    return TOOL_CALLS_HISTORY.copy()

def clear_tool_calls():
    """Clear tool call history"""
    TOOL_CALLS_HISTORY.clear()

async def setup_agent():
    print("🔗 Setting up MCP connections (async)...")
    
    # 1. Setup MultiServerMCPClient
    tools = []
    try:
        connections = {
            "budget": {"transport": "sse", "url": "http://localhost:3333/sse"},
            "destination": {"transport": "sse", "url": "http://localhost:3334/sse"},
            "weather": {"transport": "sse", "url": "http://localhost:3335/sse"},
            "currency": {"transport": "sse", "url": "http://localhost:3336/sse"},
            "calculator": {"transport": "sse", "url": "http://localhost:3337/sse"}
        }
        
        print(f"✅ Configuring {len(connections)} connections")
        
        client = MultiServerMCPClient(connections=connections)
        print("✅ MultiServerMCPClient created")
        
        # Get tools asynchronously
        raw_tools = await client.get_tools()
        print(f"📊 Successfully loaded {len(raw_tools)} raw tools")
        
        # Convert async tools to sync tools with tracking
        for tool in raw_tools:
            # Create a sync wrapper that tracks calls
            def create_tool_wrapper(tool_obj):
                def sync_wrapper(**kwargs):
                    try:
                        # Try to call the tool synchronously
                        result = tool_obj.run(kwargs)
                        track_tool_call(tool_obj.name, kwargs, result)
                        return result
                    except Exception as e:
                        # If sync fails, try async
                        try:
                            result = asyncio.run(tool_obj.arun(kwargs))
                            track_tool_call(tool_obj.name, kwargs, result)
                            return result
                        except Exception as e2:
                            error_msg = f"Tool error: {str(e2)}"
                            track_tool_call(tool_obj.name, kwargs, error_msg)
                            return error_msg
                return sync_wrapper
            
            # Create the wrapped tool
            wrapped_tool = Tool(
                name=tool.name,
                func=create_tool_wrapper(tool),
                description=tool.description
            )
            tools.append(wrapped_tool)
            print(f"  📦 {tool.name}: {tool.description[:60]}...")
            
    except Exception as e:
        print(f"❌ MCP setup failed: {e}")
        
        # Fallback to simple mock tools
        print("⚠️ Creating mock tools...")
        
        mock_tools_data = [
            ("estimate_budget", "Calculate travel budget based on destination and days"),
            ("search_destination", "Find tourist attractions and activities"),
            ("get_weather_forecast", "Get weather conditions for travel dates"),
            ("convert_currency", "Convert between different currencies"),
            ("calculate", "Perform mathematical calculations")
        ]
        
        for name, desc in mock_tools_data:
            def create_mock_func(tool_name=name, tool_desc=desc):
                def mock_func(**kwargs):
                    # Simulate different responses based on tool
                    if "budget" in tool_name:
                        result = f"Estimated budget: ${kwargs.get('days', 5) * 200} USD"
                    elif "destination" in tool_name:
                        result = f"Attractions: Main square, Museum, Local park"
                    elif "weather" in tool_name:
                        result = "Weather: Sunny, 25°C, perfect for travel"
                    elif "currency" in tool_name:
                        result = f"Converted: ${kwargs.get('amount', 100)} USD = €{kwargs.get('amount', 100) * 0.92}"
                    else:
                        result = f"Calculation result: {kwargs}"
                    
                    track_tool_call(tool_name, kwargs, result)
                    return result
                return mock_func
            
            tools.append(Tool(
                name=name,
                func=create_mock_func(),
                description=desc
            ))
        
        print(f"✅ Created {len(tools)} mock tools")
    
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
            # Get tool names for the prompt
            tool_names = ", ".join([tool.name for tool in tools])
            
            # Create the EXACT prompt template that create_react_agent expects
            prompt = PromptTemplate.from_template(
                """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
            )
            
            print(f"📝 Creating agent with {len(tools)} tools...")
            print(f"📋 Available tools: {tool_names}")
            
            # Create the agent with the prompt
            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt
            )
            
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True,
                return_intermediate_steps=True
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

# Global agent instance
_agent_executor = None

def run_travel_agent(user_request: str):
    """Run the travel planning agent"""
    global _agent_executor
    
    if _agent_executor is None:
        print("Initializing agent...")
        _agent_executor = asyncio.run(setup_agent())
    
    if not _agent_executor:
        return "Agent not initialized"
    
    try:
        print(f"\n📝 Processing: {user_request}")
        print("-" * 40)
        
        # Clear previous tool calls for this request
        clear_tool_calls()
        
        start_time = time.time()
        result = _agent_executor.invoke({"input": user_request})
        elapsed = time.time() - start_time
        
        print(f"\n✅ Response time: {elapsed:.2f}s")
        print(f"🔧 Total tool calls: {len(get_tool_calls())}")
        
        # Print tool call summary
        for i, call in enumerate(get_tool_calls()):
            print(f"  {i+1}. {call['tool']}")
        
        return result.get("output", "No output generated")
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
