"""Create all subagents using the make_graph pattern from react_agent."""
from agents.supervisor.supervisor_context import Context

from agents.react_agent.graph import make_graph
from langgraph.runtime import Runtime

async def create_subagents(runtime: Runtime[Context]):
    """Create all subagents using the make_graph pattern from react_agent."""
    
    # get values from context
    finance_model = runtime["finance_model"]
    finance_system_prompt = runtime["finance_system_prompt"]
    finance_tools = runtime["finance_tools"]
    research_model = runtime["research_model"]
    research_system_prompt = runtime["research_system_prompt"]
    research_tools = runtime["research_tools"]
    writing_model = runtime["writing_model"]
    writing_system_prompt = runtime["writing_system_prompt"]
    writing_tools = runtime["writing_tools"]
    
    # Create finance research agent using make_graph
    finance_context = Runtime(
        context={
            "model": finance_model,
            "system_prompt": finance_system_prompt,
            "selected_tools": finance_tools,
            "name": "finance_research_agent"
        }
    )
    finance_research_agent = await make_graph(finance_context)

    # Create general research agent using make_graph  
    research_context = Runtime(
        context={
            "model": research_model,
            "system_prompt": research_system_prompt,
            "selected_tools": research_tools,
            "name": "general_research_agent"
        }
    )
    general_research_agent = await make_graph(research_context)

    # Create writing agent using make_graph
    writing_context = Runtime(
        context={
            "model": writing_model,
            "system_prompt": writing_system_prompt,
            "selected_tools": writing_tools,
            "name": "writing_agent"
        }
    )
    writing_agent = await make_graph(writing_context)
    
    return [finance_research_agent, general_research_agent, writing_agent]



