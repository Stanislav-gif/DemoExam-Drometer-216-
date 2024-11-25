import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, requests
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class Request(BaseModel):
    id: int
    startDate: datetime.date
    device: str
    problemtype: str
    description: str
    client: str
    status: str

class RequestStatus(str, Enum):
    pending = "в ожидании"
    in_progress = "в работе"
    completed = "выполнено"

repo = [
    Request(id=1, 
            startDate=datetime.date(2024, 11, 1), 
            device="Ноутбук", 
            problemtype="Не включается", 
            description="Не включается экран",
            client="Иван Иванов", 
            status="в ожидании")
]
next_id = 2
app = FastAPI()

@app.get("/requests/", response_model=List[Request])
def get_requests():
    return repo

