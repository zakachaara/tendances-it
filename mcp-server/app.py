import streamlit as st
from agent_setup import run_travel_agent, get_tool_calls, clear_tool_calls
import time

st.title("🌍 Agentic Travel Planner (MCP)")

# Initialize session state
if 'planning_done' not in st.session_state:
    st.session_state.planning_done = False
if 'last_output' not in st.session_state:
    st.session_state.last_output = ""

# Input area
st.subheader("📝 Describe Your Trip")
query = st.text_area(
    "What kind of trip are you planning?",
    placeholder="Example: 'I want to visit Barcelona for 5 days with a budget of $2000'",
    height=100
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Generate Plan", type="primary", use_container_width=True):
        if query:
            with st.spinner("Planning your trip..."):
                output = run_travel_agent(query)
                st.session_state.last_output = output
                st.session_state.planning_done = True
                st.rerun()
        else:
            st.warning("Please enter a trip description")

with col2:
    if st.button("🛠️ Show Tools Used", use_container_width=True):
        st.session_state.planning_done = True
        st.rerun()

with col3:
    if st.button("🗑️ Clear All", use_container_width=True):
        clear_tool_calls()
        st.session_state.planning_done = False
        st.session_state.last_output = ""
        st.rerun()

# Show results
if st.session_state.planning_done:
    # Show tool calls
    tool_calls = get_tool_calls()
    if tool_calls:
        st.subheader("🔧 Tools Used During Planning")
        
        # Create tabs for better organization
        tab1, tab2 = st.tabs(["📋 Tool Calls", "📊 Details"])
        
        with tab1:
            for i, call in enumerate(tool_calls):
                st.markdown(f"**Step {i+1}: {call['tool']}**")
                st.text(f"Input: {call['input']}")
                st.text(f"Output: {call['output'][:200]}...")
                st.divider()
        
        with tab2:
            for i, call in enumerate(tool_calls):
                with st.expander(f"Step {i+1}: {call['tool']}"):
                    st.json(call)
    
    # Show travel plan
    if st.session_state.last_output:
        st.subheader("📋 Your Travel Plan")
        st.write(st.session_state.last_output)
        st.success("✅ Travel plan generated successfully!")

# Footer
st.markdown("---")
st.caption("Powered by LangChain, MCP, and Ollama with llama3.2:1b")
