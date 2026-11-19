from sqlalchemy import text


def query_one(conn, user_id: int) -> dict | None:
    sql = text('''
        SELECT
            id, username, display_name, email,
            created_at, last_login_at
        FROM
            users
        WHERE
            id = :id
    ''')

    params = {
        'id': user_id
    }

    result = conn.execute(sql, params)

    row = result.mappings().first()

    return dict(row) if row else None


def query_one_by_username(conn, username: str) -> dict | None:
    sql = text('''
        SELECT
            id, username, display_name, email,
            created_at, last_login_at
        FROM
            users
        WHERE
            username = :username
    ''')

    params = {
        'username': username
    }

    result = conn.execute(sql, params)

    row = result.mappings().first()

    return dict(row) if row else None


def query_one_by_email(conn, email: str) -> dict | None:
    sql = text('''
        SELECT
            id, username, display_name, email,
            created_at, last_login_at
        FROM
            users
        WHERE
            email = :email
    ''')

    params = {
        'email': email
    }

    result = conn.execute(sql, params)

    row = result.mappings().first()

    return dict(row) if row else None


def query_many(conn, limit: int, offset: int) -> list[dict]:
    sql = text('''
        SELECT
            id, username, display_name, email,
            created_at, last_login_at
        FROM
            users
        ORDER BY id
        LIMIT :limit
        OFFSET :offset
    ''')

    params = {
        'limit': limit,
        'offset': offset
    }

    result = conn.execute(sql, params)
    rows = result.mappings().all()

    return [dict(r) for r in rows]


def count_all(conn) -> int:
    sql = text('''
        SELECT
            COUNT(*)
        FROM
            users
    ''')

    return conn.execute(sql).scalar_one()


def insert_user(conn, username: str, display_name: str | None, email: str) -> int:
    sql = text('''
        INSERT INTO users(username, display_name, email)
        VALUES (:username, :display_name, :email)
    ''')

    params = {
        'username': username,
        'display_name': display_name,
        'email': email,
    }

    result = conn.execute(sql, params)

    return result.lastrowid


# 传 None 的字段保持原值，无法把字段改成 NULL
def update_user(conn, user_id: int, display_name: str | None, email: str | None) -> int:
    sql = text('''
        UPDATE
            users
        SET
            display_name = COALESCE(:display_name, display_name),
            email = COALESCE(:email, email)
        WHERE
            id = :id
    ''')

    params = {
        'display_name': display_name,
        'email': email,
        'id': user_id
    }

    result = conn.execute(sql, params)

    return result.rowcount


def username_exists(conn, username: str) -> bool:
    sql = text('''
        SELECT 1
        FROM
            users
        WHERE
            username = :username
    ''')

    params = {
        'username': username
    }

    row = conn.execute(sql, params).mappings().first()

    return row is not None


def email_exists(conn, email: str) -> bool:
    sql = text('''
        SELECT 1
        FROM
            users
        WHERE
            email = :email
    ''')

    params = {
        'email': email
    }

    row = conn.execute(sql, params).mappings().first()

    return row is not None


def delete_user(conn, user_id: int) -> int:
    sql = text('''
        DELETE FROM
            users
        WHERE
            id = :id
    ''')

    params = {
        'id': user_id
    }

    result = conn.execute(sql, params)

    return result.rowcount
