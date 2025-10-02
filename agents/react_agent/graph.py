"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add Context and implement using a make_graph function to rebuild the graph at runtime.
"""
from agents.react_agent.tools import get_tools
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from agents.react_agent.context import Context
from langgraph.runtime import Runtime



async def make_graph(runtime: Runtime[Context]):
    
    # Runtime is passed as a dict by the API, create Context from it (This will be fixed in the next release of langgraph-api)
    context = Context(**runtime)
    llm = context.model
    selected_tools = context.selected_tools
    prompt = context.system_prompt
    
    # specify the name for use in supervisor architecture
    agent_name = context.name

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