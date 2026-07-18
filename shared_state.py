from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class SharedState(TypedDict):
    genre : str
    user_query: str
    search_topic: str
    search_query: str

    messages: Annotated[List[BaseMessage], add_messages]

    relevant_results: bool

    final_output: str