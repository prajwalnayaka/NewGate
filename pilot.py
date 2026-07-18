import os, time
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
from pprint import pp
from pydantic import BaseModel, Field

load_dotenv()

API_KEY=os.getenv("GOOGLE_API_KEY")
CHAT_MODEL=os.getenv("GEMINI_3.5_F")

class TavilySearchInput(BaseModel):
    query: str = Field(..., description="The actual search query which is used to browse the internet.")
    topic:str = Field(..., description="The general topic of the query")

@tool("Tavily_Web_Search", args_schema=TavilySearchInput)
def browse(query,topic):
    """Function to use Tavily Search API. Allows to search the internet about a specific topic based on a query."""
    tavily=TavilySearch(max_results=5,topic=topic)
    results=tavily.invoke({"query":f"{topic} {query}"})
    return results

system_prompt="""You are a helpful AI agent. Your goal is to figure out the topic about which the user is asking questions and form a concise query for web search about it.

Present the news exactly in this format for each item:
**[Headline]**
[3-5 sentences of short summary]
*Source: [Source URL or Name]*

Provide exactly the requested number of updates."""

since=time.time()
gemini=create_agent(model=CHAT_MODEL,tools=[browse],system_prompt=system_prompt)
result=gemini.invoke(
    {"messages":[
        {"role":"user",
         "content":"Regional news about Bangalore"}
    ]}
)
# for msg in result["messages"]:
#     print(f"\n{'='*20} {type(msg).__name__} {'='*20}")
#     if hasattr(msg, "tool_calls") and msg.tool_calls:
#         print(f"Tool call: {msg.tool_calls}")
#     if isinstance(msg.content, list):
#         for block in msg.content:
#             print(block.get("text", block))
#     else:
#         print(msg.content)
pp(result['messages'][-2].content)
""" result["messages"][-1]=AIMessage
     ""        ""     [-2]=ToolMessage"""
print(f"{(time.time()-since)/60:.2f} (mm:ss)")