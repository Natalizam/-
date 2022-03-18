from fastapi import FastAPI, Depends
import psycopg2
import uvicorn
from psycopg2.extras import RealDictCursor

app = FastAPI()


def get_db():
    with psycopg2.connect(
        user="robot-startml-ro",
        password="pheiph0hahj1Vaif",
        host="postgres.lab.karpov.courses",
        port=6432,
        database="startml",
    ) as conn:
        return conn


@app.get("/user")
def get_user(limit, conn=Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            f"""
            SELECT *
            FROM "user"
            LIMIT {limit}
            """
        )
        return cur.fetchall()


if __name__ == '__main__':
    uvicorn.run(app)