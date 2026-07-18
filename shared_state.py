from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
import operator

class Article(TypedDict):
    title: str
    genre: str
    publish_date: str
    content: str
    source: str


class SharedState(TypedDict):
    genre : list[str]
    # user_query: str
    search_topic: str
    search_query: str
    retry_count: int

    selected_articles: Annotated[list[Article], operator.add]

    messages: Annotated[list[BaseMessage], add_messages]

    relevant_results: bool

    final_output: dict[str]