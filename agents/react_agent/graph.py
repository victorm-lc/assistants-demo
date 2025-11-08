"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add Context and implement using a make_graph function to rebuild the graph at runtime.
"""
from agents.react_agent.tools import get_tools
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from agents.react_agent.context import Context
from langgraph.runtime import Runtime



async def make_graph(runtime: Runtime[Context]):
    
    # Runtime is passed as a dict by the API, create Context from it. Currently this is not support by the langgraph-api but will be in the near future.
    # context = runtime.context
    # llm = context.model
    # selected_tools = context.selected_tools
    # prompt = context.system_prompt
    
    # # specify the name for use in supervisor architecture
    # agent_name = context.name

    # Workaround for Now: Get values from runtime.get("configurable") which is a dict of the configurable parameters
    configurable = runtime.get("configurable", {})
    llm = configurable.get("model", "anthropic:claude-haiku-4-5")
    selected_tools = configurable.get("selected_tools", ["get_todays_date"])
    prompt = configurable.get("system_prompt", "You are a helpful AI assistant.")
    agent_name = configurable.get("name", "react_agent")

    # Compile the builder into an executable graph
    # You can customize this by adding interrupt points for state updates
    graph = create_agent(
        model=init_chat_model(llm), 
        tools=get_tools(selected_tools),
        system_prompt=prompt, 
        context_schema=Context,
        name=agent_name
    )

    return graph