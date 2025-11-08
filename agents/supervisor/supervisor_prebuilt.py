"""
NOTE: This file uses create_supervisor, which is NO LONGER the recommended pattern for multi-agent systems.

RECOMMENDED PATTERN: Use subagents as tools (tool calling pattern)
See: https://docs.langchain.com/oss/python/langchain/multi-agent

Why we're still using create_supervisor here:
- Easier visualization in LangGraph Studio
- Simpler to understand the supervisor architecture
- Better Studio support for this pattern (subagent-as-tools visualization coming soon)

For production systems, prefer wrapping subagents as tools for better control flow and type safety.
"""

from langgraph.runtime import Runtime
from agents.supervisor.supervisor_context import Context
from agents.supervisor.subagents import create_subagents
from langchain.chat_models import init_chat_model

from langgraph_supervisor import create_supervisor

# Main graph construction
async def make_supervisor_graph(runtime: Runtime[Context]):
    
    # Runtime is passed as a dict by the API. Currently this is not support by the langgraph-api but will be in the near future.
    # context = runtime.context
    # supervisor_model = context.supervisor_model
    # supervisor_system_prompt = context.supervisor_system_prompt
    
    # Workaround for Now: Get values from runtime.get("configurable") which is a dict of the configurable parameters
    configurable = runtime.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "anthropic:claude-haiku-4-5")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a supervisor coordinating specialized agents.")
    
    # Create subagents using the new async function, passing runtime dict
    subagents = await create_subagents(runtime)

    # Create supervisor graph
    supervisor_graph = create_supervisor(
        agents=subagents,
        model=init_chat_model(supervisor_model),
        prompt=supervisor_system_prompt,
        config_schema=Context   
    )

    compiled_graph = supervisor_graph.compile()
    return compiled_graph
