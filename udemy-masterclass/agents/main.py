from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tools

load_dotenv()

chat = ChatOpenAI()
tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=f"You are an AI that has access to a SQLite database.\n{tables}"
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
tools = [run_query_tool, describe_tables_tools]
"""
Agent
- A chain that knows how to use tools
- Will take that list of tools and convert them into JSON function descriptions
- Still has input variables, memory, prompts, etc - all the normal things a chain has
"""
agent = OpenAIFunctionsAgent(llm=chat, prompt=prompt, tools=tools)
"""
Agent Executor
- Takes an agent and runs it until the response is not a function call
- Essentially a function while loop
"""
agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

agent_executor("How many users have provided a shipping address?")
