"""Create all subagents using the make_graph pattern from react_agent."""
from agents.supervisor.supervisor_context import Context as SupervisorContext
from agents.react_agent.context import Context as ReactContext

from agents.react_agent.graph import make_graph
from langgraph.runtime import Runtime

async def create_subagents(runtime: Runtime[SupervisorContext]):
    """Create all subagents using the make_graph pattern from react_agent."""
    
    # Runtime is passed as a dict by the API, create Context from it (This will be fixed in the next release of langgraph-api)
    context = SupervisorContext(**runtime)

    # get values from context
    finance_model = context.finance_model
    finance_system_prompt = context.finance_system_prompt
    finance_tools = context.finance_tools
    research_model = context.research_model
    research_system_prompt = context.research_system_prompt
    research_tools = context.research_tools
    writing_model = context.writing_model
    writing_system_prompt = context.writing_system_prompt
    writing_tools = context.writing_tools
    
    # Create finance research agent using make_graph
    # Pass as dict since make_graph expects dict from API
    finance_research_agent = await make_graph({
        "model": finance_model,
        "system_prompt": finance_system_prompt,
        "selected_tools": finance_tools,
        "name": "finance_research_agent"
    })

    # Create general research agent using make_graph  
    general_research_agent = await make_graph({
        "model": research_model,
        "system_prompt": research_system_prompt,
        "selected_tools": research_tools,
        "name": "general_research_agent"
    })

    # Create writing agent using make_graph
    writing_agent = await make_graph({
        "model": writing_model,
        "system_prompt": writing_system_prompt,
        "selected_tools": writing_tools,
        "name": "writing_agent"
    })
    
    return [finance_research_agent, general_research_agent, writing_agent]



