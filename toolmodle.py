import os
from unittest import result

from dotenv import load_dotenv
from langchain.tools import tool
from zai import ZhipuAiClient

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("未找到 API_KEY，请检查 .env 文件")

_client = ZhipuAiClient(api_key=API_KEY)   # 全局复用，不要每次调用都新建


@tool
def web_search(
    search_query: str,
    count: int = 10,
    domain_filter: str = "",
) -> str:
    """使用智谱 Web Search 联网搜索，获取最新的网页信息。

    Args:
        search_query: 搜索关键词，例如 "论坛热度最高的游戏"。
        count: 返回结果数量，1~10，默认 10。
        domain_filter: 限制搜索域名，例如 "bbs.nga.cn"；空字符串表示不限制。

    Returns:
        搜索结果的文本摘要（标题 + 链接 + 摘要拼接），供 LLM 阅读。
    """
    kwargs = {
        "search_query": search_query,
        "search_engine": "search_pro",
        "count": min(count, 10),
    }
    if domain_filter:
        kwargs["search_domain_filter"] = domain_filter

    resp = _client.web_search.web_search(**kwargs)

    # 具体字段以实际返回为准，下面按常见结构做拼接
    items = getattr(resp, "search_result", None) or getattr(resp, "results", [])
    lines = []
    for it in items:
        title = getattr(it, "title", "")
        url = getattr(it, "link", "") or getattr(it, "url", "")
        summary = getattr(it, "content", "") or getattr(it, "summary", "")
        lines.append(f"标题：{title}\n链接：{url}\n摘要：{summary}\n")
    return "\n".join(lines) if lines else str(resp)





