"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add Context and implement using a make_graph function to rebuild the graph at runtime.
"""
from agents.react_agent.tools import get_tools
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from agents.react_agent.context import Context
from langgraph.runtime import Runtime



async def make_graph(runtime: Runtime[Context]):
    
    # get values from context - they're in runtime['configurable'] in the prerelease
    configurable = runtime.get("configurable", {})
    llm = configurable.get("model", "anthropic:claude-sonnet-4-5-20250929")
    selected_tools = configurable.get("selected_tools", ["get_todays_date"])
    prompt = configurable.get("system_prompt", "You are a helpful AI assistant.")
    
    # specify the name for use in supervisor architecture
    agent_name = configurable.get("name", "react_agent")

    # Compile the builder into an executable graph
    # You can customize this by adding interrupt points for state updates
    graph = create_agent(
        model=init_chat_model(llm), 
        tools=get_tools(selected_tools),
        prompt=prompt, 
        context_schema=Context,
        name=agent_name
    )

    return graph