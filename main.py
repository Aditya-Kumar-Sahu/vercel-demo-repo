from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd

class Output(BaseModel):
    marks : list[int]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )

data = pd.read_json("q-vercel-python.json")

@app.get("/")
async def root():
    return "Hello Guys!!!!!"

@app.get("/api", response_model=Output)
async def get_marks(name: List[str] = Query(...)):
    result = []
    for n in name:
        try:
            result.append(int(data.loc[data['name']==n]['marks'].iloc[0]))
        except IndexError:
            pass
    return {"marks": result}


if __name__ == '__main__':
    import uvicorn as uv
    uv.run(app=app)