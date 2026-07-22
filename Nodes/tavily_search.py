import logging, dotenv, os
from google import genai
from google.genai import types
from tavily import TavilyClient
from pydantic import BaseModel
from states import BranchState

dotenv.load_dotenv()

class SearchParams(BaseModel):
    search_query: str
    search_topic: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
logger = logging.getLogger(__name__)

gemini=genai.Client(api_key=GEMINI_API_KEY)
tavily_service = TavilyClient(api_key=TAVILY_API_KEY)

def gemini_generate_search_params(genre):
    genre=genre
    prompt=f"""Create a short and concise search_query and search_topic for the Tavily API about {genre} to get the latest news and developments. 
Set the search_topic as either one of 'news','general' or 'finance' based on the relevancy to the genre. Your reply must only consist of the key-value pairs for 
search_query and search_topic."""
    response=gemini.models.generate_content(model="gemini-2.5-flash",contents=prompt,config=types.GenerateContentConfig(
        response_mime_type="application/json",response_schema=SearchParams
    ))

    if response:
        search_params: SearchParams = response.parsed
        search_query=search_params.search_query
        search_topic=search_params.search_topic
        logger.info(f"Gemini successfully generated the search parameters for Tavily.")
        return search_query, search_topic.lower()
    else:
        logger.error(f"Gemini failed to generate the search parameters for Tavily.")
        return None, None

def tavily_search_node(state: BranchState):
    genre=state['genre']
    retry_count=state['retry_count']
    if retry_count>0:
        logger.info(f"Retry attempt {retry_count} of Tavily search for {genre}.")
    search_query, search_topic = gemini_generate_search_params(genre)
    if not search_query:
        logger.error(f"Search query wasn't generated for by Gemini.")
        return {"search_query": None, "search_topic": None, "raw_search_results": []}
    tavily_results=tavily_service.search(query=search_query,topic= search_topic, max_results=10)
    raw_results=tavily_results.get('results',[]) if tavily_results else []
    if raw_results:
        logger.info(f"Tavily search successfully generated results.")
        return {"search_query":search_query,
                "search_topic":search_topic,
                "raw_search_results": raw_results}
    else:
        logger.error(f"Tavily search failed to generate results.")
        return {"search_query":None,"search_topic":None,"raw_search_results": []}