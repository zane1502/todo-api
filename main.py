from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Task(BaseModel):
    id: int
    name: str = Field(min_length=1)
    done: bool

class UserTask(BaseModel):
    name: str = Field(min_length=1)
    done: bool = False

total_tasks = [
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
    return total_tasks

@app.get("/tasks/{id}", response_model=Task)
async def get_task(id: int):

    for task in total_tasks:
        if task.id == id:
            return task

    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"The ID: {id} was not found."
    )

@app.post("/tasks", status_code= status.HTTP_201_CREATED)
async def create_task(task: UserTask):
    task_id: int = len(total_tasks) + 1
    task_name = task.name
    done = task.done

    user_task = Task(id= task_id,
                     name= task_name,
                     done= done)
    
    total_tasks.append(user_task.model_dump())

    return user_task