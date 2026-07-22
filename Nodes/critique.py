import logging, dotenv, os
from google import genai
from google.genai import types
from pydantic import BaseModel
from states import BranchState

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini=genai.Client(api_key=GEMINI_API_KEY)

class CritiqueDecision(BaseModel):
    is_good: bool

def critique_node(state: BranchState):
    genre=state['genre']
    search_query=state['search_query']
    retry_count=state['retry_count']
    branch_end_result=state['branch_end_result']
    if not branch_end_result:
        logger.error("One or more branches did not generate structured output.")
        return{"good_results": False, "retry_count": retry_count+1}
    else:
        prompt=f"""Evalute whether the search results below are good enough to be part of a news digest. The search query for the results is: '{search_query}'
        and genre is: '{genre}'. The evaluation should be based on the relevancy, recency, robustness and so on of the results strictly with respect to the 
        query. Your response should be boolean only.
        Search Results:
        {branch_end_result}"""
        try:
            response=gemini.models.generate_content(model="gemini-3.5-flash",contents=prompt,config=types.GenerateContentConfig(
                response_mime_type='application/json',response_schema=CritiqueDecision
            ))
            critique_decision=response.parsed.is_good
        except Exception as e:
            logger.error(f"Could not generate critique decision. Error: {e}")
            return {"good_results": None}

        if critique_decision:
            logger.info("Critique node accepted the results.")
            return {"good_results": critique_decision}
        else:
            logger.info("Critique node rejected the results.")
            return {"good_results": critique_decision, "retry_count": retry_count + 1}