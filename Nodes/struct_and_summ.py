import logging, dotenv, os
from google import genai
from google.genai import types
from pydantic import BaseModel
from states import BranchState, Article

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini=genai.Client(api_key=GEMINI_API_KEY)

class ArticleModel(BaseModel):
    title: str
    genre: str
    publish_date: str
    content: str
    source: str

class ArticleList(BaseModel):
    articles: list[ArticleModel]

def gemini_struct_and_summ(genre, raw_search_results):
    genre=genre
    raw_search_results=raw_search_results
    prompt=f"""Following are the internet search results for the genre '{genre}'.
    
    {raw_search_results}
    
    Select the top 3-5 best search results based on criteria such as relevancy to the genre,
     discarding of duplicate coverage, low-information content and so on. Summarize the content into 4-6 concise and meaningful sentences which are easy to understand. Your final output 
     must contain the following key-value pairs only:
     
     'title': A suitable title for the article
     'genre': {genre}
     'publish_date': Publish date of the article
     'content': Summarized content of the article
     'source': Source of the article if possible else 'NA'
     
        """
    response=gemini.models.generate_content(model="gemini-3.1-flash-lite",contents=prompt,config=types.GenerateContentConfig(
        response_mime_type="application/json",response_schema=ArticleList
    ))
    if response:
        logger.info(f"{genre} | Gemini successfully parsed the raw search results and structured and summarized them into a single list.")
        return [article.model_dump() for article in response.parsed.articles]
    else:
        logger.error(f"{genre} | Gemini failed to parse the raw search results.")
        return None


def structure_and_summarize_node(state: BranchState):
    genre=state['branch_genre']
    raw_search_results=state['raw_search_results']
    if not raw_search_results:
        logger.error(f"{genre} | No raw search results to summarize (Tavily Search Node Error?)")
        return{"branch_end_result":[]}
    structured_summarized=gemini_struct_and_summ(genre, raw_search_results)
    if not structured_summarized:
        logger.error(f"{genre} | Gemini could not parse the search results.")
        return{"branch_end_result":[]}
    logger.info(f"{genre} | Successfully summarized and restructured the raw search results.")
    return{"branch_end_result":structured_summarized}