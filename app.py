import datetime
from typing import Optional
from fastapi import FastAPI, requests
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class Request(BaseModel):
    id: int
    date_added: datetime.datetime
    device: str
    problemtype: str
    description: str
    client: str
    status: str #в ожидании,в работе,выполнено

repo = []

app = FastAPI()

message = ""

@app.post("/requests/", response_model=Request)
def get_requests(param: Optional[int] = None):
    if param:
        return {"repo": [o for o in repo if o.number == param]}
    return {"repo": repo}