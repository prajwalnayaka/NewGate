import os, time
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
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
Use the available tool for accomplishing the goal of getting the user their answers."""

since=time.time()
gemini=create_agent(model=CHAT_MODEL,tools=[browse])
result=gemini.invoke(
    {"messages":[
        {"role":"user",
         "content":"What are the latest developments regarding ChatGPT 5.6 Sol?"}
    ]}
)
for msg in result["messages"]:
    print(f"\n{'='*20} {type(msg).__name__} {'='*20}")
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print(f"Tool call: {msg.tool_calls}")
    if isinstance(msg.content, list):
        for block in msg.content:
            print(block.get("text", block))
    else:
        print(msg.content)
print(f"{(time.time()-since)/60:.2f} (mm:ss)")