''''' App to manage todo list'''
'''from datetime import date
import os
from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uvicorn

from pymongo.errors import ServerSelectionTimeoutError
from utils.db_connect import Dbconnect 
from services.add_todo import AddTodo 
from services.view_todo import View
from services.delete_todo_item import Delete

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
db=Dbconnect().mongodb_conn_get()
# Dependency
def get_collection(name: str):
    return db[name]

# Create a new todo item
@app.post("/todos/", response_model=TodoItemInDB)
async def create_todo_item(todo: TodoItemCreate, collection=Depends(lambda: get_collection("todos"))):
    todo_dict = todo.dict()
    result = await collection.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    return todo_dict

# Get a todo item by ID
@app.get("/todos/{todo_id}", response_model=TodoItemInDB)
async def read_todo_item(todo_id: str, collection=Depends(lambda: get_collection("todos"))):
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo["id"] = str(todo["_id"])
    return todo

# Update a todo item
@app.put("/todos/{todo_id}", response_model=TodoItemInDB)
async def update_todo_item(todo_id: str, todo: TodoItemUpdate, collection=Depends(lambda: get_collection("todos"))):
    update_dict = {k: v for k, v in todo.dict().items() if v is not None}
    result = await collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return {**update_dict, "id": todo_id}

# Delete a todo item
@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo_item(todo_id: str, collection=Depends(lambda: get_collection("todos"))):
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return {"detail": "Todo item deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

# main.py
from fastapi import FastAPI, Depends
from repositories.todo_repository import TodoRepository
from services.todo_service import TodoService
from pymongo import MongoClient
from models.todo_models import TodoItemCreate, TodoItemUpdate, TodoItemInDB
from fastapi import FastAPI, Depends, HTTPException
from utils.db_connect import Dbconnect

app = FastAPI()
db=Dbconnect().mongodb_conn_get()
# Dependency
def get_todo_repository() -> TodoRepository:
    return TodoRepository(db["todos"])

def get_todo_service(repository: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    return TodoService(repository)

@app.post("/todos/", response_model=TodoItemInDB)
async def create_todo_item(todo: TodoItemCreate, service: TodoService = Depends(get_todo_service)):
    print("started")
    return await service.create_todo_item(todo)

@app.get("/todos/{todo_id}", response_model=TodoItemInDB)
async def read_todo_item(todo_id: str, service: TodoService = Depends(get_todo_service)):
    return await service.get_todo_item(todo_id)

@app.put("/todos/{todo_id}", response_model=TodoItemInDB)
async def update_todo_item(todo_id: str, todo: TodoItemUpdate, service: TodoService = Depends(get_todo_service)):
    return await service.update_todo_item(todo_id, todo)

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo_item(todo_id: str, service: TodoService = Depends(get_todo_service)):
    success = await service.delete_todo_item(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return {"detail": "Todo item deleted"}
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

