import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, Form, HTTPException
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
            status="в ожидании"),
    Request(id=2, 
            startDate=datetime.date(2024, 11, 1), 
            device="Телефон", 
            problemtype="Не включается", 
            description="Не включается экран",
            client="Александр Иванов", 
            status="в ожидании"),
]

next_id = 3

app = FastAPI()

@app.get("/requests", response_model=List[Request])
def get_requests():
    return repo
@app.get("/requests/{request_id}", response_model=Request)
def get_request(request_id: int):
    for db_request in repo:
        if db_request.id == request_id:
            return db_request
    raise HTTPException(status_code=404, detail="Заявка не найдена")

@app.post("/requests")
def create_request(
    id: int = Form(...),
    startDate: str = Form(...), 
    device: str = Form(...),
    problemtype: str = Form(...),
    description: str = Form(...),
    client: str = Form(...),
    status: str = Form(...)
):
    new_request = Request(
        id=id,
        startDate=startDate,
        device=device,
        problemtype=problemtype,
        description=description,
        client=client,
        status=status
    )
    repo.append(new_request)
    return new_request