import datetime
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
    status: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[str] = None
    comments: Optional[List[str]] = None


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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

message = ""

@app.get("/requests")
def get_request(param: Optional[int] = None):
    global message
    buffer = message
    message = ""
    if param:
        return {"repo": [o for o in repo if o.id == param], "message": buffer}
    return {"repo": repo, "message": buffer}

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
def update_request(
    number: int = Form(...),
    status: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    assignee: Optional[str] = Form(None),
    comments: Optional[List[str]] = Form(None)
):
    global message
    for o in repo:
        if o.id == number:
            if status and status != o.status:
                o.status = status
                message += f"Статус заявки №{o.id} изменен\n"
                if o.status == "выполнено":
                    message += f"Заявка №{o.id} завершена\n"
                    o.endDate = datetime.datetime.now().date()
            if description is not None:
                o.description = description
            if assignee is not None:
                o.assignee = assignee
            if comments is not None:
                o.comments.extend(comments)
            return o
    raise HTTPException(status_code=404, detail="Заявка не найдена")


def count_completed_requests():
    return len([request for request in repo if request.status == "выполнено"])

def get_problem_type_statistics():
    problem_type_count = {}
    for request in repo:
        if request.problemtype in problem_type_count:
            problem_type_count[request.problemtype] += 1
        else:
            problem_type_count[request.problemtype] = 1
    return problem_type_count

def calculate_average_completion_time():
    completion_times = [
        (request.endDate - request.startDate).days 
        for request in repo 
        if request.status == "выполнено"
    ]
    if count_completed_requests() != 0:
        return sum(completion_times) / count_completed_requests()
    return 0

@app.get("/statistics")
def get_statistics():
    return {
        "completed_requests_count": count_completed_requests(),
        "problem_type_statistics": get_problem_type_statistics(),
        "average_completion_time": calculate_average_completion_time()
    }
