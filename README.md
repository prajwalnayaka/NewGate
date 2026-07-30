
# NewGate
___ 
### NewGate is an AI powered news aggregator which fetches the latest and relevant news about the user selected genres from across the internet without relying on any one specific news outlet. 



### Abstract System Overview
___

It is a **hybrid** agentic AI and AI workflow system, allowing AI to participate in sourcing, tidying and critiquing the news articles which will be presented to the user.

## Screenshots
___




## How It Works
___

- There are 2 distinct and separate LangGraph graphs at play. The parent graph acts as the web that houses all the children graphs.

- The parent graph oversees the end-to-end flow of operations, guided by the SharedState. This is the 'user selected genres to articles' pipeline but the **parent graph doesn't have the capacity to generate the end results itself**. 

- The childred graphs or the branches are **spawned by the Send objects** in the first node the parent graph. 

- Send object **creates the required 'metadata'** fields for each genre, which is then passed to created branch.   

- Each branch gets a **copy of the BranchState** which just one genre, therefore each genre gets its own branch. 

- **These branches run concurrently, meaning that the runtime with this parallel setting is significantly less when compared to a sequential '*one genre after another*' approach**. 

- Each branch with it's respective follows the following sequence:
    - Tavily Search Node: Use Gemini API to **generate genre specific search parameters** and use them to **fetch articles from the internet using Tavily Search API**.

    - Stucturing and Summarizing Node: Use Gemini API to **reorganize the messy articles** into a **uniform format** which is easy to read and has relevant information, such as **publishing date, source** and so on.

    - Critique Node: Use Gemini API to have an **LLM read the structured and summarized articles and give a verdict about whether the results are informative and relevant to the genre**. 

    - Conditional Edge: If the **critique node accepts the results, the branch merges** it's genre specific into the selected articles pool of the SharedState. If the **critique node rejects the results, the branch retries** all the way back from Tavily Search Node. There is a maximum **retry limit of 3**, this is to ensure that the graph **doesn't run indefinitely**.    

    - Aggregation Node: The end results are in the seleted articles pool, the aggregation takes these results/articles and reorganizes them into a final output dictionary with specific structure. 

- FastAPI App: The FastAPI app hosts the NewGate backend and accept a list of genres and returns a JSON object with the fetched news in it.

- Streamlit Frontend: The user facing UI tranfers the user selected genres to the FastAPI backend in the form of a POST request and displays the news articles, grouped by genre.
## Tech Stack
___

**AI:** LangGraph, Google Gemini API

**Internet Search API:** Tavily

**Backend:** FastAPI

**Frontend:** Streamlit


## Run It Locally
___

I recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/). 

```bash
uv sync
fastapi dev
streamlit run frontend/front_app.py
```


## Future Scope
___

The potential future work for this project lies in setting this up as a daily routine, where the system would each registered user an email of a newsletter covering the user selected genres. The frequency of the newsletter could also be decided by the user. 