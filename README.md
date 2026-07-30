
# NewGate
___ 
### NewGate is an AI powered news aggregator which fetches the latest and relevant news about the user selected genres from across the internet. It does so without relying on any one specific news outlet. 



### Abstract System Overview
___

It is a **hybrid** agentic AI and AI workflow system, allowing AI to participate in sourcing, tidying and critiquing the news articles which will be presented to the user.

## Why hybrid?
___
The line between an agentic system and an AI workflow is pretty blurry. From my observation, the more one tries to control and standardize the behaviour of a supposed agentic AI system, the more deterministic it gets. Therefore, I believe the best way
to incorporate the agentic AI paradigm is to have a blend of deterministic AI workflows; which perform a specific task in a highly predictable manner and have an  agentic AI layer on top of it to govern the deterministic pipelines. This could be through giving the agent the 
liberty to make simple yes/no decisions for a specific task's flow of execution, selecting the appropriate pipeline to run, decisions based on result/data validation and so on. 

In the case of NewGate, the workflow from 'genre-to-articles' is highly deterministic and doesn't require AI agency but only needs AI capability. The part where AI agency really shines is the critique node, there the AI has a validation call to make. If it deems the results as good, the process moves onto results staging.
Whereas if it rejects the results, the 'genre-to-articles' deterministic AI workflow is run again, thus exhibiting AI agency to make decisions based on information and task at hand.

## Screenshots
___
- Landing Page
  <img width="1917" height="961" alt="Landing" src="https://github.com/user-attachments/assets/0b9b1bb1-98b1-4a49-8c6e-4c4eb8fbfcf6" />
- Genre Selection
  <img width="1917" height="967" alt="Selecting_genres" src="https://github.com/user-attachments/assets/130c47e4-56ec-4022-96ba-ec602ec3dbd6" />
- Fetching
  <img width="1917" height="962" alt="Fetching" src="https://github.com/user-attachments/assets/55c3a6da-88ed-4540-9ed9-5b294b04f756" />
- Unexpanded Results
  <img width="1917" height="971" alt="Result_un" src="https://github.com/user-attachments/assets/4e8a246a-c1d7-473a-b8b2-9c8035868f1d" />
- Expanded Results
    <img width="1912" height="967" alt="Result_ex" src="https://github.com/user-attachments/assets/4d42390a-4a9f-4e24-8398-4db42311802a" />
- Error Handling
  <img width="1917" height="967" alt="Error_1" src="https://github.com/user-attachments/assets/3acb71dc-1567-405e-a974-6ec41ec83881" />



## How It Works
___
<img width="1461" height="2838" alt="Graph" src="https://github.com/user-attachments/assets/806e67e5-2383-444a-ac7b-f186657a2ac9" />


- There are 2 distinct and separate LangGraph graphs at play. The parent graph acts as the web that houses all the child graphs.

- The parent graph oversees the end-to-end flow of operations, guided by the SharedState. This is the 'user selected genres to articles' pipeline but the **parent graph doesn't have the capacity to generate the end results by itself**. 

- The child graphs or the branches are **spawned by the Send objects** in the first node the parent graph. 

- Send object **creates the required 'metadata'** fields for each genre, which is then passed to created branch.   

- Each branch gets a **copy of the BranchState** with just one genre, therefore each genre gets its own branch. 

- **These branches run concurrently, meaning that the runtime with this parallel setting is significantly less when compared to a sequential '*one genre after another*' approach**. 

- Each branch with its respective genre and copy of BranchState, follows the following sequence:
    - Tavily Search Node: Use Gemini API to **generate genre specific search parameters** and use them to **fetch articles from the internet using Tavily Search API**.

    - Stucturing and Summarizing Node: Use Gemini API to **reorganize the messy articles** into a **uniform format** which is easy to read and has relevant information, such as **publishing date, source** and so on.

    - Critique Node: Use Gemini API to have an **LLM read the structured and summarized articles and give a verdict about whether the results are informative and relevant to the genre**. 

    - Conditional Edge: If the **critique node accepts the results, the branch merges** it's genre-specific into the selected articles pool of the SharedState. If the **critique node rejects the results, the branch retries** all the way back from Tavily Search Node. There is a maximum **retry limit of 3**, this is to ensure that the graph **doesn't run indefinitely**.    

    - Aggregation Node: The end results are in the selected articles pool, the aggregation takes these results/articles and reorganizes them into a final output dictionary with specific structure. 
    - Error Handling Node: If a **branch couldn't produce results** due issues like API usage limits or a node failure, that **branch's specific genre's status is shows the error message in the expandable tab**. However, **this doesn't affect the results of the other genres; meaning even if one genre has no results, the other genres whose branches worked perfectly fine will display the articles**. 

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
