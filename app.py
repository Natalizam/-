from fastapi import FastAPI, Depends
import psycopg2
import uvicorn
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

app = FastAPI()


def get_db():
    with psycopg2.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DATABASE"),
    ) as conn:
        return conn


@app.get("/user")
def get_user(limit, conn=Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT *
            FROM "user"
            LIMIT %(limit_users)s
            """,
            {"limit_users": limit}
        )
        return cur.fetchall()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
