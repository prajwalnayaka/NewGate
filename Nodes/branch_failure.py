from states import BranchState

def branch_failure_handler_node(state: BranchState):
    genre=state["branch_genre"]
    return {
        "branch_end_result": [],
        "branch_statuses": [
            {"genre": genre, "message": f"Couldn't fetch content for {genre}. Could be due to usage limits of API(s)."}]
    }