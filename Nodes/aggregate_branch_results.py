import logging, dotenv, os
from states import *

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
logger = logging.getLogger(__name__)

def aggregate_branch_results_node(state: BranchState):
    branch_results = state["branch_end_result"]
    if branch_results:
        logger.info("Branch produced results; contributing to shared pool.")
        return {"selected_articles": list(branch_results)}
    else:
        logger.info("Branch produced no results to contribute.")
        return {"selected_articles": []}