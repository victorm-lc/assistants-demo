"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add configuration and implement using a make_graph function to rebuild the graph at runtime.
"""
from agents.react_agent.tools import get_tools
from langchain.agents import create_agent
from agents.utils import load_chat_model

from agents.react_agent.context import Context
from langgraph.runtime import Runtime



async def make_graph(runtime: Runtime[Context]):
    
    # get values from configuration
    llm = runtime.context.model
    selected_tools = runtime.context.selected_tools
    prompt = runtime.context.system_prompt
    
    # specify the name for use in supervisor architecture
    agent_name = runtime.context.name

    # Compile the builder into an executable graph
    # You can customize this by adding interrupt points for state updates
    graph = create_agent(
        model=load_chat_model(llm), 
        tools=get_tools(selected_tools),
        prompt=prompt, 
        context_schema=Context,
        name=agent_name
    )

    return graph