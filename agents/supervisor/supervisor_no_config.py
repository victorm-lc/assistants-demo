from langgraph.prebuilt import create_react_agent
from agents.react_agent.tools import finance_research, basic_research_tool, advanced_research_tool, get_todays_date
from langchain_openai import ChatOpenAI

from langgraph_supervisor import create_supervisor


# Finance sub-agent prompt
finance_system_prompt="""You are an expert finance research assistant for a digital content agency.
You have access to the following tools: finance_research, basic_research, and get_todays_date. 
First get today's date then continue. 
The finance_research tool is used to search for financial data and news from Yahoo Finance. 
The basic_research tool is used to search for general information. 
The get_todays_date tool is used to get today's date. 
When you are done with your research, return the research to the supervisor agent."""

finance_model = ChatOpenAI(model="gpt-4o")
finance_tools = [finance_research, basic_research_tool, get_todays_date]

finance_agent = create_react_agent(
    model=finance_model,
    tools=finance_tools,
    prompt=finance_system_prompt,
    name="finance_research_agent"
)

# Research sub-agent prompt
research_system_prompt="""You are an expert general research agent. You have access to the following tools: 
advanced_research_tool and get_todays_date. First get today's date then continue to use the advanced_research_tool tool to search 
for general information on the topic you are given to research, when your done you return the research to the supervisor 
agent. YOU MUST USE THE ADVANCED_RESEARCH_TOOL TO GET THE INFORMATION YOU NEED"""

research_model = ChatOpenAI(model="gpt-4o")
research_tools = [advanced_research_tool, get_todays_date]

research_agent = create_react_agent(
    model=research_model,
    tools=research_tools,
    prompt=research_system_prompt,
    name="general_research_agent"
)


# Supervisor prompt
supervisor_system_prompt = """

You are the Executive Content Director orchestrating a team of specialized AI agents to produce exceptional content for clients.

Available agents:
- finance_research_agent: Specialized in financial data research and analysis using Yahoo Finance and other financial sources
- general_research_agent: Expert at comprehensive web research on any topic using advanced search tools

Your process:
1. Analyze the user's request to understand what type of content they need
2. If needed, route to appropriate research agents to gather information
3. When the task is complete, you can respond back to the user!

Always be strategic about which agents to use and in what order to produce the best possible content."""

supervisor_model = ChatOpenAI(model="gpt-4o")

supervisor_graph = create_supervisor(
        agents=[finance_agent, research_agent],
        model=supervisor_model,
        prompt=supervisor_system_prompt,
    )

graph = supervisor_graph.compile()
