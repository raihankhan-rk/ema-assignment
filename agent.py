import langchain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
import time
from tools import data_query, generate_personalized_email, get_lead_activity_summary, get_lead_info, get_industry_wise_lead_count, get_lead_source_distribution, send_email
from prompts import system_prompt
from dotenv import load_dotenv

load_dotenv()

search = DuckDuckGoSearchRun()
# Define the tools
tools = [data_query,
         get_lead_activity_summary,
         get_lead_info, search,
         generate_personalized_email,
         get_industry_wise_lead_count,
         get_lead_source_distribution,
         send_email]

# Define the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind_tools(tools)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True
)

while (user_input := input("Enter a prompt (q to quit): ")) != "q":
    now = time.time()
    response = agent_executor.invoke({"input": user_input})
    print(f"Agent: {response['output']}")
    print(f"Time taken: {time.time() - now}")
