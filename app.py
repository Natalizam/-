from fastapi import FastAPI, Depends
import uvicorn
import psycopg2
import os
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

app = FastAPI()


def get_db():
    # .env
    with psycopg2.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("POSTGRES_DATABASE"),
    ) as conn:
        return conn


# Инъекция
@app.get("/user")
def get_user(limit, conn: connection = Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:  # type: cursor
        cur.execute(
            f"""
            SELECT * FROM "user" LIMIT {limit}
            """,
            # {"limit": limit}
        )
        return cur.fetchall()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
