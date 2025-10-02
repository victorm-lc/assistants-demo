from langgraph.runtime import Runtime
from agents.supervisor.supervisor_context import Context
from agents.supervisor.subagents import create_subagents
from langchain.chat_models import init_chat_model

from langgraph_supervisor import create_supervisor

# Main graph construction
async def make_supervisor_graph(runtime: Runtime[Context]):
    # Extract context values directly from the config
    configurable = runtime.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "anthropic:claude-sonnet-4-5-20250929")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful AI assistant.")
    
    # Create subagents using the new async function, passing configurable values
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
