import datetime
from enum import Enum
from typing import Annotated, List, Optional
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Request(BaseModel):
    id: int
    startDate: datetime.date
    device: str
    problemtype: str
    description: str
    client: str
    status: str
    endDate: Optional[datetime.date] = None
    assignee: Optional[str] = None  # Ответственный за выполнение
    comments: Optional[List[str]] = []

class UpdateRequestDTO(BaseModel):
    number: int 
    status: Optional[str] = ""
    description: Optional[str] = ""
    assignee: Optional[str] = ""
    comments: Optional[str] = str

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

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)


message = ""

@app.get("/requests")
def get_request(param = None):
    global message
    buffer = message
    message = ""
    if(param):
        return { "repo": [o for o in repo if o.id == int(param)],"message": message}
    return {"repo" : repo ,"message" : buffer}

@app.get("/requests/{request_id}", response_model=Request)
def get_request(request_id: int):
    for db_request in repo:
        if db_request.id == request_id:
            return db_request
    raise HTTPException(status_code=404, detail="Заявка не найдена")

@app.post("/requests", response_model=Request)
def create_request(
    startDate: str = Form(...), 
    device: str = Form(...),
    problemtype: str = Form(...),
    description: str = Form(...),
    client: str = Form(...),
    status: str = Form(...)
):
    global next_id
    new_request = Request(
        id=next_id,
        startDate=datetime.datetime.strptime(startDate, "%Y-%m-%d").date(),  
        device=device,
        problemtype=problemtype,
        description=description,
        client=client,
        status=status
    )
    repo.append(new_request)
    next_id += 1 
    return new_request

@app.post("/update")
def update_request(dto: Annotated[UpdateRequestDTO , Form()]):
    global message
    for o in repo:
        if o.id == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
                message += f"Статус заявки №${o.number} изменен\n"
                if(o.status == "выполнено"):
                    message += f"Заявки №{o.number} Завершено\n"
                    o.endDate = datetime.datetime.now()
            if dto.description != "":
                o.description = dto.description
            if dto.assignee != "":
                o.assignee = dto.assignee
            if dto.comments != None and dto.comments != "":
                o.comments.append(dto.comments)
            return o
    return "Не найдено"