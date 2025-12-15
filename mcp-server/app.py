import streamlit as st
from agent_setup import run_travel_agent

st.title("🌍 Agentic Travel Planner (MCP)")

query = st.text_input("Describe your trip (e.g., 'Plan a 5-day trip to Barcelona with budget')")

if st.button("Plan My Trip"):
    with st.spinner("Planning your trip..."):
        output = run_travel_agent(query)
    st.subheader("📋 Your Travel Plan")
    st.write(output)
    st.success("Done!")
