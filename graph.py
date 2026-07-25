from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from states import SharedState, BranchState
from Nodes import *

def flow_router(state: BranchState):
    if state['good_results']:
        return "done"
    elif state['good_results'] is None:
        return "possible_usage_exhaustion"
    elif state['retry_count']>3:
        return "give_up"
    else:
        return "retry"


graph=StateGraph(SharedState)

# Adding Nodes
graph.add_node("tavily_search",tavily_search_node)
graph.add_node("structure_and_summary",structure_and_summarize_node)
graph.add_node("crtique_AI",critique_node)
graph.add_node("aggregate_branch_results",aggregate_branch_results_node)

# Adding Edges
graph.add_edge(START,"tavily_search")
graph.add_edge("tavily_search","structure_and_summary")
graph.add_edge("structure_and_summary","critique_AI")
graph.add_edge("some_compiler_node?",END)

# Add conditional edge
graph.add_conditional_edges("critique_AI",flow_router,{
    "retry":"tavily_search",
    "done":"aggregate_branch_results",
    "give_up":"some_exception_handler_node?",
    "possible_usage_exhaustion":"some_exception_handler_node?"
})

app=graph.compile()

news=app.invoke({"genre":["technology","finance","gaming","international affairs"]})
print(news['final_output'])