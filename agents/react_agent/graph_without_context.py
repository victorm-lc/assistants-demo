from agents.react_agent.tools import basic_research, get_todays_date
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# initialize our model and tools    
llm = init_chat_model(model="openai:gpt-5-mini")
tools = [basic_research, get_todays_date]
prompt = """
    You are a helpful AI assistant trained in creating engaging social media content!
    you have access to two tools: basic_research and get_todays_date. Please get_todays_date then 
    perform any research if needed, before generating a social media post.
"""

# Compile the builder into an executable graph
graph = create_agent(
    model=llm, 
    tools=tools, 
    prompt=prompt,
    name="react_agent"
)