from langgraph.runtime import Runtime
from agents.supervisor.supervisor_context import Context
from agents.supervisor.subagents import create_subagents
from langchain.chat_models import init_chat_model

from langgraph_supervisor import create_supervisor

# Main graph construction
async def make_supervisor_graph(runtime: Runtime[Context]):
    
    # Runtime is passed as a dict by the API, create Context from it (This will be fixed in the next release of langgraph-api)
    context = Context(**runtime)
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
