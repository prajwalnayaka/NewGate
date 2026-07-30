from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from graph import app

class Genres(BaseModel):
    genres: list[str]

web_app = FastAPI()

@web_app.get("/home")
def home():
    return JSONResponse({"project":"NewGate",
                         "you_are_at":"/home",
                         "status":"good"})

@web_app.post("/run")
def news(genres: Genres):
    request=genres.genres
    try:
        news=app.invoke({"genre":request,"selected_articles":[],"branch_statuses":[]})
        return JSONResponse({"news":news['final_output']},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))