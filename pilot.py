import os, time
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

load_dotenv()

API_KEY=os.getenv("GEMINI_API_KEY")
CHAT_MODEL=os.getenv("GEMINI_3.1_F")

gemini=init_chat_model(CHAT_MODEL,api_key=API_KEY)
since=time.time()
output=gemini.invoke("Do you read me?")
print(output.content[0].get("text"))
print(f"{(time.time()-since)/60:.2f} (mm:ss)")