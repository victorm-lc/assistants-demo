"""
Create all subagents using the make_graph pattern from react_agent.

NOTE: These subagents are used with create_supervisor, which is NOT the recommended pattern.

RECOMMENDED: Wrap subagents as tools using the @tool decorator instead.
See: https://docs.langchain.com/oss/python/langchain/multi-agent

This older langgraph-supervisor approach is kept for easier visualization in LangGraph Studio.
For production, use the tool calling pattern for better control flow and type safety.
"""
from agents.supervisor.supervisor_context import Context as SupervisorContext
from agents.react_agent.context import Context as ReactContext

from agents.react_agent.graph import make_graph
from langgraph.runtime import Runtime

async def create_subagents(runtime: Runtime[SupervisorContext]):
    """Create all subagents using the make_graph pattern from react_agent."""
    
    # Runtime is passed as a dict by the API, create Context from it. Currently this is not support by the langgraph-api but will be in the near future.
    # context = runtime.context

     # get values from context
    # finance_model = context.finance_model
    # finance_system_prompt = context.finance_system_prompt
    # finance_tools = context.finance_toolsd
    # research_model = context.research_model
    # research_system_prompt = context.research_system_prompt
    # research_tools = context.research_tools
    # writing_model = context.writing_model
    # writing_system_prompt = context.writing_system_prompt
    # writing_tools = context.writing_tools

    
    # Workaround for Now: Get values from runtime.get("configurable") which is a dict of the configurable parameters
    configurable = runtime.get("configurable", {})

    finance_model = configurable.get("finance_model", "anthropic:claude-haiku-4-5")
    finance_system_prompt = configurable.get("finance_system_prompt", "You are a financial research assistant.")
    finance_tools = configurable.get("finance_tools", ["finance_research", "basic_research", "get_todays_date"])
    research_model = configurable.get("research_model", "anthropic:claude-haiku-4-5")
    research_system_prompt = configurable.get("research_system_prompt", "You are a research assistant.")
    research_tools = configurable.get("research_tools", ["advanced_research", "get_todays_date"])
    writing_model = configurable.get("writing_model", "anthropic:claude-haiku-4-5")
    writing_system_prompt = configurable.get("writing_system_prompt", "You are a writing assistant.")
    writing_tools = configurable.get("writing_tools", ["basic_research", "get_todays_date"])

    
    # Create finance research agent using make_graph
    # Pass as dict wrapped in "configurable" since make_graph expects dict from API
    finance_research_agent = await make_graph({
        "configurable": {
            "model": finance_model,
            "system_prompt": finance_system_prompt,
            "selected_tools": finance_tools,
            "name": "finance_research_agent"
        }
    })

    # Create general research agent using make_graph  
    general_research_agent = await make_graph({
        "configurable": {
            "model": research_model,
            "system_prompt": research_system_prompt,
            "selected_tools": research_tools,
            "name": "general_research_agent"
        }
    })

    # Create writing agent using make_graph
    writing_agent = await make_graph({
        "configurable": {
            "model": writing_model,
            "system_prompt": writing_system_prompt,
            "selected_tools": writing_tools,
            "name": "writing_agent"
        }
    })
    
    return [finance_research_agent, general_research_agent, writing_agent]



