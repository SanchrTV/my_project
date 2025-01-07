from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

app = FastAPI(
    title="TODO Service",
    description="Сервис для управления задачами",
    version="1.0.0"
)

DB_PATH = os.getenv("DB_PATH", "/app/data/app.db")

class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/items", response_model=TodoItem)
def create_item(item: TodoItem):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO todo_items (title, description, completed)
        VALUES (?, ?, ?)
    """, (item.title, item.description, item.completed))
    conn.commit()
    item.id = cur.lastrowid
    conn.close()
    return item

@app.get("/items", response_model=List[TodoItem])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo_items")
    items = cur.fetchall()
    conn.close()
    return [TodoItem(**dict(row)) for row in items]
