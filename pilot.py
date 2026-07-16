import os, time
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
from pprint import pp
#from pydantic import BaseModel

load_dotenv()

API_KEY=os.getenv("GOOGLE_API_KEY")
CHAT_MODEL=os.getenv("GEMINI_3.5_F")

@tool("Tavily_Web_Search")
def browse(query,topic):
    """Function to use Tavily Search API. Allows to search the internet about a specific topic based on a query."""
    tavily=TavilySearch(max_results=10,topic=topic)
    results=tavily.invoke({"query":query})
    return results

system_prompt="""You are a helpful AI agent, you're goal is to figure out the topic about which the user is asking questions about and form a concise query for web search about it.
Use the available tool for accomplishing the goal of getting the user their answers. Present the news in this format: Clear and concise headline followed by 3-5 sentences of short summary and mention the source at the end."""

since=time.time()
gemini=create_agent(model=CHAT_MODEL,tools=[browse])
result=gemini.invoke(
    {"messages":[
        {"role":"user",
         "content":"Get me the top 5 headlines about the Indian stock market."}
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
pp(result['messages'][-1].content)
print(f"{(time.time()-since)/60:.2f} (mm:ss)")