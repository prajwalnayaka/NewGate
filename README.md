
# NewGate
___ 
### NewGate is an AI powered news aggregator which fetches the latest and relevant news about the user selected genres from across the internet. It does so without relying on any one specific news outlet. 



### Abstract System Overview
___

It is a **hybrid** agentic AI and AI workflow system, allowing AI to participate in sourcing, tidying and critiquing the news articles which will be presented to the user.

## Screenshots
___


## Why hybrid?
___
The line between an agentic system and an AI workflow is pretty blurry. From my observation, more on tries to control and standardize the behaviour of a supposed agentic AI system, the more deterministic the system becomes. Therefore, I believe the best way
to incorporate the agentic AI paradigm is to have a blend of deterministic AI workflows, which perform a specific task in a highly predictable manner and then have an  agentic AI approach to govern the deterministic pipelines. This could be through giving the agent the 
liberty to answer simple yes/no decisions for some task's flow of execution, selecting the appropriate pipeline to run, decisions based result/data validation and so on. 

In the case of NewGate, the workflow from 'genre-to-articles' is highly deterministic and doesn't require AI agency but only needs AI capability. The part where AI agency really shines is the critique node, there the AI has a validation call to make. If it deems the results as good, the process moves onto results staging.
Whereas if it rejects the results, the 'genre-to-articles' deterministic AI workflow is run again, thus exhibiting AI agency to make decisions based on information and taks at hand.

## How It Works
___

- There are 2 distinct and separate LangGraph graphs at play. The parent graph acts as the web that houses all the children graphs.

- The parent graph oversees the end-to-end flow of operations, guided by the SharedState. This is the 'user selected genres to articles' pipeline but the **parent graph doesn't have the capacity to generate the end results itself**. 

- The children graph or the branches are **spawned by the Send objects** in the first node the parent graph. 

- Send object **creates the required 'metadata'** fields for each genre, which is then passed to created branch.   

- Each branch gets a **copy of the BranchState** which just one genre, therefore each genre gets its own branch. 

- **These branches run concurrently, meaning that the runtime with this parallel setting is significantly less when compared to a sequential '*one genre after another*' approach**. 

- Each branch with its respective genre and copy of BranchState, follows the following sequence:
    - Tavily Search Node: Use Gemini API to **generate genre specific search parameters** and use them to **fetch articles from the internet using Tavily Search API**.

    - Stucturing and Summarizing Node: Use Gemini API to **reorganize the messy articles** into a **uniform format** which is easy to read and has relevant information, such as **publishing date, source** and so on.

    - Critique Node: Use Gemini API to have an **LLM read the structured and summarized articles and give a verdict about whether the results are informative and relevant to the genre**. 

    - Conditional Edge: If the **critique node accepts the results, the branch merges** it's genre specific into the selected articles pool of the SharedState. If the **critique node rejects the results, the branch retries** all the way back from Tavily Search Node. There is a maximum **retry limit of 3**, this is to ensure that the graph **doesn't run indefinitely**.    

    - Aggregation Node: The end results are in the selected articles pool, the aggregation takes these results/articles and reorganizes them into a final output dictionary with specific structure. 

- FastAPI App: The FastAPI app hosts the NewGate backend and accept a list of genres and returns a JSON object with the fetched news in it.

- Streamlit Frontend: The user facing UI transfers the user selected genres to the FastAPI backend in the form of a POST request and displays the news articles, grouped by genre.
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

The potential future work for this project lies in setting this up as a daily routine, where the system would send each registered user an email of a newsletter covering the user selected genres. The frequency of the newsletter could also be decided by the user. 