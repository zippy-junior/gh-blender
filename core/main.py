from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

mesh = None

class OBJData(BaseModel):
    v: List
    f: List


@app.post("/obj")
def process_obj(data: OBJData):
    global mesh
    mesh = data

@app.get("/obj")
def get_obj():
    global mesh
    return mesh

