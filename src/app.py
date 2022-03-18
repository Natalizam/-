from fastapi import FastAPI, Depends
import yaml
import uvicorn
import psycopg2
import os
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path
# DIRTY HACK
import sys
sys.path.append(str(Path(__file__).parent.parent))
############

from src.crud import get_likes, get_feed
app = FastAPI()


def get_db() -> cursor:
    # .env
    with psycopg2.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DATABASE"),
        cursor_factory=RealDictCursor,
    ) as conn:
        return conn


def config():
    print(__file__)
    with open(Path(__file__).parent.parent / "params.yaml", "r") as f:
        return yaml.safe_load(f)


# Инъекция
@app.get("/user")
def get_user(limit, conn: connection = Depends(get_db)):
    with conn.cursor() as cur:  # type: cursor
        cur.execute(
            f"""
            SELECT * FROM "user" LIMIT %(limit)s
            """,
            {"limit": limit}
        )
        return cur.fetchall()


@app.get("/user/feed")
def get_user_feed(user_id: int, limit: int = 10, conn: connection = Depends(get_db), config: dict = Depends(config)):
    return get_feed(conn, user_id, limit, config)


@app.get("/user/likes")
def get_user_feed(user_id: int, limit: int = 10, conn: connection = Depends(get_db), config: dict = Depends(config)):
    print(config)
    return get_likes(conn, user_id, limit, config)


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
