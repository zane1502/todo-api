from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    name: str
    done: float

complete_tasks = [
    Task(id = 1, name= "Laundry", done = True),
    Task(id= 2, name= "Market errands", done= True),
    Task(id= 3, name= "Cooking", done= True),
    ]

@app.get("/")
async def root():
    return {"name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"]
            }

@app.get("/health")
async def root():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return complete_tasks

@app.get("/tasks/{id}", response_model=Task)
async def get_task(id: int):

    for task in complete_tasks:
        if task.id == id:
            return task

    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"The ID: {id} was not found."
    )
