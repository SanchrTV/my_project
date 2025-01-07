from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import shortuuid
from starlette.responses import RedirectResponse

app = FastAPI(
    title="Short URL Service",
    description="Сервис сокращения длинных ссылок",
    version="1.0.0"
)

DB_PATH = os.getenv("DB_PATH", "/app/data/app.db")

class URLRequest(BaseModel):
    url: str

class URLInfo(BaseModel):
    short_id: str
    full_url: str

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            short_id TEXT PRIMARY KEY,
            full_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/shorten", response_model=URLInfo)
def shorten_url(url_request: URLRequest):
    short_id = shortuuid.ShortUUID().random(length=6)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (short_id, full_url) VALUES (?, ?)",
                (short_id, url_request.url))
    conn.commit()
    conn.close()
    return URLInfo(short_id=short_id, full_url=url_request.url)

@app.get("/{short_id}")
def redirect_to_full(short_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_url FROM urls WHERE short_id = ?", (short_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return RedirectResponse(url=row["full_url"])
    raise HTTPException(status_code=404, detail="Short URL not found")
