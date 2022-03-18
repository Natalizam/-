def get_likes(conn, user_id, limit, config):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM feed_action
            WHERE user_id = %(user_id)s
                AND action = 'like'
                AND time >= %(start_date)s
            ORDER BY time 
            LIMIT %(limit)s
            """,
            {"user_id": user_id, "limit": limit, "start_date": config["feed_start_date"]}
        )
        return cur.fetchall()


def get_feed(conn, user_id, limit, config):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM feed_action
            WHERE user_id = %(user_id)s
                AND time >= %(start_date)s
            ORDER BY time 
            LIMIT %(limit)s
            """,
            {"user_id": user_id, "limit": limit, "start_date": config["feed_start_date"]}
        )
        return cur.fetchall()
