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
    
    # Runtime is passed as a dict by the API, create Context from it (This will be fixed in the next release of langgraph-api)
    context = runtime.context
    supervisor_model = context.supervisor_model
    supervisor_system_prompt = context.supervisor_system_prompt
    
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
