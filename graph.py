from pprint import pprint
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


# ------------------------------ BRANCH GRAPH --------------------------------------- #

branch_graph=StateGraph(BranchState)

# Adding Nodes
branch_graph.add_node("tavily_search", tavily_search_node)
branch_graph.add_node("structure_and_summary", structure_and_summarize_node)
branch_graph.add_node("critique_AI", critique_node)
branch_graph.add_node("aggregate_branch_results", aggregate_branch_results_node)
branch_graph.add_node("branch_failure_handler", branch_failure_handler_node)

# Adding Edges
branch_graph.add_edge(START, "tavily_search")
branch_graph.add_edge("tavily_search", "structure_and_summary")
branch_graph.add_edge("structure_and_summary", "critique_AI")
branch_graph.add_edge("aggregate_branch_results", END)
branch_graph.add_edge("branch_failure_handler", END)

# Add conditional edge
branch_graph.add_conditional_edges("critique_AI", flow_router, {
    "retry":"tavily_search",
    "done":"aggregate_branch_results",
    "give_up":"branch_failure_handler",
    "possible_usage_exhaustion":"branch_failure_handler",
})

compiled_branch=branch_graph.compile()
# ----------------------------------------------------------------------------------- #


# ------------------------------ PARENT GRAPH --------------------------------------- #

def fan_out(state: SharedState):
    return [Send("run_branch", {"branch_genre": g, "retry_count": 0, "good_results": False}) for g in state["genre"]]



parent_graph=StateGraph(SharedState)


parent_graph.add_node("run_branch", compiled_branch)
parent_graph.add_node("final_output_staging", final_output_staging_node)


parent_graph.add_conditional_edges(START,fan_out ,["run_branch"])
parent_graph.add_edge("run_branch","final_output_staging")
parent_graph.add_edge("final_output_staging",END)


app=parent_graph.compile()

# ----------------------------------------------------------------------------------- #

news=app.invoke({"genre":['technology','gaming','Indian Stock Market'],"selected_articles":[],"branch_statuses":[]})
pprint(news['final_output'])