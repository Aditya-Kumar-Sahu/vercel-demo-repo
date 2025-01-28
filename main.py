from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd

class Marks(BaseModel):
    marks : List[int]


class Student(BaseModel):
    studentId   : int
    class_      : str = Field(..., alias="class")

    class Config:
        populate_by_name = True


class Students(BaseModel):
    students : List[Student]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )

data1 = pd.read_json("q-vercel-python.json")
data2 = pd.read_csv("q-fastapi.csv")

@app.get("/")
async def root() -> str:
    return "Hello Guys!!!!!"

@app.get("/v1/api", response_model=Marks)
async def get_marks(name: List[str] = Query(...)) -> Marks:
    result : List[int] = []
    for n in name:
        try:
            result.append(int(data1.loc[data1['name']==n]['marks'].iloc[0]))
        except IndexError:
            pass
    return Marks(marks=result)


@app.get("/v2/api", response_model=Students)
async def get_students(class_: Optional[List[str]] = Query(None)) -> Students:
    if class_:
        # Filter by class if provided
        filtered_data = data2[data2["class"].isin(class_)]
    else:
        # Return all students if no class filter
        filtered_data = data2

    # Convert to JSON-compatible response
    records = filtered_data.rename(columns={"class": "class_"}).to_dict(orient="records")
    return Students(students=records)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", reload=True)