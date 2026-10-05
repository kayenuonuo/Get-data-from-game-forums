import os
from dotenv import load_dotenv
# 清理冗余import，只保留必要包
from langchain_openai import ChatOpenAI
# 1.x 正确导入
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
# 导入你的自定义搜索工具
from toolmodle import web_search

load_dotenv()
API_KEY = os.getenv("API_KEY")

# 初始化LLM GLM-5.2
llm = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/", # 一定要加上智谱的接口地址！
    model="glm-5.2",
    temperature=0.1
)

# 用ChatPromptTemplate，搭配create_openai_tools_agent（支持模板，不会报你之前的pydantic错误）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个游戏信息观察员，负责通过联网搜索获取最新数据，分析哪些游戏目前最火爆。回答要基于搜索结果，不要编造信息"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [web_search]
# 创建agent（新版api，接收prompt模板）
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)



def ask (question: str) -> str:  # ← 关键：必须有这个函数
    result =agent_executor.invoke({"input": question})
    return result["output"]