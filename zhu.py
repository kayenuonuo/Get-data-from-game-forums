import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate

from toolmodle import web_search

load_dotenv()
API_KEY = os.getenv("API_KEY")


llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/", 
    model="glm-5.2",
    temperature=0.1
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个游戏信息观察员，负责通过联网搜索获取最新数据，分析哪些游戏目前最火爆。回答要基于搜索结果，不要编造信息"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [web_search]

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)



def ask (question: str) -> str:  
    result =agent_executor.invoke({"input": question})
    return result["output"]
