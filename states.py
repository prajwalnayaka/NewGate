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

    selected_articles: Annotated[list[Article], operator.add]

    messages: Annotated[list[BaseMessage], add_messages]


    final_output: dict[str]


class BranchState(TypedDict):
    genre: str
    search_topic: str
    search_query: str
    good_results: bool
    retry_count: int
    raw_search_results: list[dict]
    branch_end_result: list[Article]