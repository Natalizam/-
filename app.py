from fastapi import FastAPI, Depends
import uvicorn
import psycopg2
import os
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

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
def get_user_feed(user_id: int, limit: int = 10, conn: connection = Depends(get_db)):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM feed_action
            WHERE user_id = %(user_id)s
                AND time >= '2021-12-01'
            ORDER BY time 
            LIMIT %(limit)s
            """,
            {"user_id": user_id, "limit": limit}
        )
        return cur.fetchall()


@app.get("/user/likes")
def get_user_feed(user_id: int, limit: int = 10, conn: connection = Depends(get_db)):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM feed_action
            WHERE user_id = %(user_id)s
                AND action = 'like'
                AND time >= '2021-12-01'
            ORDER BY time 
            LIMIT %(limit)s
            """,
            {"user_id": user_id, "limit": limit}
        )
        return cur.fetchall()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
