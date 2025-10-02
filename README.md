# LangGraph Configuration Patterns Demo

> **📹 Coming from the YouTube video?** This repository has been **updated for LangGraph V1** (released October 2025). The core concepts remain the same, but the implementation has changed to use the new `Runtime[Context]` pattern instead of `RunnableConfig`. See the [Migration Guide](#migration-from-video-to-current-version) section below for details on what changed.

This project demonstrates **how to implement runtime configuration patterns** in ReAct Agents and supervisor-style architectures using [LangGraph](https://docs.langchain.com/). It shows the progression from hardcoded agents to flexible, configurable systems.


## Configuration Pattern Progression

This demo showcases three approaches to agent configuration:

### 1. **No Configuration** (`agents/react_agent/graph_without_context.py`)
- Hardcoded ReAct agent
- Fixed model, prompt, and tools
- Simple but inflexible

### 2. **Single Agent Configuration** (`agents/react_agent/graph.py`)
- Dynamic runtime configuration via `Runtime[Context]`
- Configurable models, prompts, and tools
- Clean `runtime.context` pattern

### 3. **Multi-Agent Configuration** (`agents/supervisor/`)
- Supervisor orchestrating multiple configured agents
- Each subagent uses the same configuration pattern
- Shows how configuration scales to complex architectures

## What it demonstrates

### Configuration Evolution
1. **Start simple**: Hardcoded values for quick prototyping
2. **Add flexibility**: Runtime configuration for different use cases  
3. **Scale complexity**: Same configuration patterns across multiple agents

### Key Configuration Patterns
- **Context schemas**: Typed classes (Pydantic, TypedDict, dataclass, etc.) define available configuration options
- **Runtime parameter**: `runtime: Runtime[Context]` provides typed access
- **Direct access**: `runtime.context` for typed configuration values
- **Default values**: Defined in your chosen schema type (e.g., Pydantic Fields, dataclass defaults)
- **Reusable functions**: Same `make_graph(runtime)` pattern everywhere

## Migration from Video to Current Version

If you're coming from the YouTube video (recorded Jul 2, 2025), here are the key changes:

### What Changed in LangGraph V1

**Old Pattern (from video):**
```python
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

async def make_graph(config: RunnableConfig):
    configurable = config.get("configurable", {})
    llm = configurable.get("model", "openai/gpt-4")
    selected_tools = configurable.get("selected_tools", ["get_todays_date"])
    prompt = configurable.get("system_prompt", "You are a helpful assistant.")
    
    graph = create_react_agent(
        model=load_chat_model(llm), 
        tools=get_tools(selected_tools),
        prompt=prompt
    )
    return graph
```

**New Pattern (current):**
```python
from langgraph.runtime import Runtime
from pydantic import BaseModel, Field
from langchain.agents import create_agent

# Define Context schema (this example uses Pydantic, but TypedDict, dataclass, etc. also work)
class Context(BaseModel):
    model: str = Field(default="openai:gpt-4")
    selected_tools: list[str] = Field(default=["get_todays_date"])
    system_prompt: str = Field(default="You are a helpful assistant.")

async def make_graph(runtime: Runtime[Context]):
    
    graph = create_agent(
      # Access typed configuration via runtime.context
        model=init_chat_model(runtime.context.model), 
        tools=get_tools(runtime.context.selected_tools),
        prompt=runtime.context.system_prompt,
        context_schema=Context
    )
    return graph
```

**Note on Agent Creation:** The video used `create_react_agent` from `langgraph.prebuilt`. This has been **replaced with `create_agent`** from `langchain.agents` as part of LangGraph V1's consolidation of agent functionality into the LangChain library.

**Note on Model Loading:** The video used a custom `load_chat_model()` helper function with `provider/model` format (e.g., `"openai/gpt-4"`). This has been replaced with direct use of `init_chat_model()` which now supports `provider:model` format (e.g., `"openai:gpt-5"`), eliminating the need for the helper function.

### Key Differences

| Aspect | Old (Video) | New (Current) |
|--------|-------------|---------------|
| **Config Type** | `RunnableConfig` (dict-based) | `Runtime[Context]` (typed object) |
| **Function** | `create_react_agent` | `create_agent` |
| **Import** | `from langgraph.prebuilt` | `from langchain.agents` |
| **Schema Definition** | Optional `Configuration` class | Required `Context` class (examples use Pydantic) |
| **Schema Usage** | Optional `config_schema` param | Required `context_schema` param |
| **Access** | `config.get("configurable", {})` | `runtime.context` |
| **Type Safety** | Runtime checks | Compile-time type hints |

### Why the Change?

LangGraph V1 introduced stronger typing and cleaner APIs:
- ✅ **Better IDE support** - autocomplete and type hints with typed `runtime.context`
- ✅ **Type safety** - catch configuration errors at compile time
- ✅ **Clearer APIs** - explicit context schemas define available options
- ✅ **Flexibility** - use Pydantic, TypedDict, dataclass, or any typed class

The **core concepts from the video remain valid** - the way you think about configuring agents and building supervisor architectures hasn't changed, just the implementation details.

## Configuration in Action

### Single Agent Configuration
```python
from langgraph.runtime import Runtime
from pydantic import BaseModel, Field

# Define Context schema (using Pydantic in this example)
class Context(BaseModel):
    model: str = Field(default="anthropic/claude-sonnet-4-5-20250929")
    system_prompt: str = Field(default="You are a helpful AI assistant.")
    selected_tools: list[str] = Field(default=["get_todays_date"])

async def make_graph(runtime: Runtime[Context]):
    # Access typed configuration from runtime
    context = runtime.context
    
    return create_agent(
        model=init_chat_model(context.model), 
        tools=get_tools(context.selected_tools), 
        prompt=context.system_prompt,
        context_schema=Context
    )
```

### Multi-Agent Configuration
```python
async def create_subagents(runtime: Runtime[SupervisorContext]):
    # Access supervisor configuration
    context = runtime.context
    
    # Create subagents with their own configurations
    finance_agent = await make_graph(
        Runtime(context=ReactContext(
            model=context.finance_model,
            system_prompt=context.finance_system_prompt,
            selected_tools=context.finance_tools
        ))
    )
    # ... more agents using same pattern
```

## Why This Approach?

### ✅ **Type Safety**
- IDE autocomplete and type hints with `runtime.context`
- Compile-time type checking with typed Context objects
- Optional validation with Pydantic if desired

### ✅ **Simplicity**
- Clean Context schemas define available configuration options
- Direct access via `runtime.context`
- Easy to understand and modify

### ✅ **Consistency** 
- Same pattern for single and multi-agent systems
- Reusable `make_graph()` function
- Predictable configuration structure

### ✅ **Flexibility**
- Runtime configuration changes
- Easy to add new configuration options
- Works with LangGraph Studio

### ✅ **Scalability**
- Pattern works from simple to complex architectures
- No architectural debt when scaling up
- Clean separation of concerns

## Getting Started

Assuming you have already [installed LangGraph Studio](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download), to set up:

1. **Install dependencies**:
   ```bash
   # Create and activate a virtual environment and install dependencies.
   uv sync
   source .venv/bin/activate
   ```

2. **Create a `.env` file**:
   ```bash
   cp .env.example .env
   ```

3. **Define required API keys** in your `.env` file.
4. **Run LangGraph Studio Locally**
   ```bash
   langgraph dev
   ```

The primary search tool uses [Tavily](https://tavily.com/). Create an API key [here](https://app.tavily.com/sign-in).

<!--
Setup instruction auto-generated by `langgraph template lock`. DO NOT EDIT MANUALLY.
-->

### Setup Model

The defaults values for `model` are shown below:

```yaml
model: anthropic/claude-3-5-sonnet-latest
```

Follow the instructions below to get set up, or pick one of the additional options.

#### Anthropic

To use Anthropic's chat models:

1. Sign up for an [Anthropic API key](https://console.anthropic.com/) if you haven't already.
2. Once you have your API key, add it to your `.env` file:

```
ANTHROPIC_API_KEY=your-api-key
```
#### OpenAI

To use OpenAI's chat models:

1. Sign up for an [OpenAI API key](https://platform.openai.com/signup).
2. Once you have your API key, add it to your `.env` file:
```
OPENAI_API_KEY=your-api-key
```

<!--
End setup instructions
-->

4. Customize whatever you'd like in the code.
5. Open the folder in LangGraph Studio!

## Exploring the Configuration Patterns

### Start with No Configuration
Examine `agents/react_agent/graph_without_context.py` to see the hardcoded baseline.

### Add Single Agent Configuration  
Look at `agents/react_agent/graph.py` to see how runtime configuration is added while keeping the code simple.

### Scale to Multi-Agent Configuration
Explore `agents/supervisor/` to see how the same runtime configuration patterns work with multiple specialized agents.

## Development

### Configuration Best Practices Shown

- **Direct dictionary access** over complex configuration classes
- **Default values** for graceful fallbacks  
- **Consistent patterns** across different complexity levels
- **Runtime flexibility** without architectural complexity

### Local Development

While iterating on your configuration:
- Test different models and prompts via configuration
- Add new tools by updating the `selected_tools` list
- Create new agent types using the same configuration pattern
- Debug configuration issues in LangGraph Studio

## Documentation

You can find the latest LangChain, LangGraph and LangSmith documentation [here](https://docs.langchain.com/), including examples and references for configuration patterns.

## About This Repository

This repository demonstrates configuration patterns for **LangGraph V1** (October 2024). It has been updated from the original YouTube video version to use the new `Runtime[Context]` pattern with typed context schemas (using Pydantic in the examples) and `runtime.context` access, which provides better type safety and IDE support while maintaining the same core architectural concepts.

The migration from `RunnableConfig` → `Runtime[Context]` represents LangGraph's evolution toward stronger typing and better developer experience, coordinated with the LangChain ecosystem. Note that while this repository uses Pydantic for context schemas, you can use TypedDict, dataclass, or any typed class.