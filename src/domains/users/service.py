from sqlalchemy.exc import IntegrityError

from src.utils.exceptions import BusinessError
from src.core.db import db
from src.domains.users import repository


def get_user(user_id: int) -> dict:
    with db.connect() as conn:
        user = repository.query_one(conn, user_id)
    if user is None:
        raise BusinessError('user not found')
    return user


def list_users(limit: int) -> list[dict]:
    with db.connect() as conn:
        users = repository.query_many(conn, limit)
    return users


def create_user(username: str, display_name: str | None, email: str) -> int:
    with db.connect() as conn:
        if repository.username_exists(conn, username):
            raise BusinessError('username already exists')
        if repository.email_exists(conn, email):
            raise BusinessError('email already exists')
        try:
            user_id = repository.insert_user(conn, username, display_name, email)
            conn.commit()
        except IntegrityError as exc:
            # 预检漏网的竞态：唯一键是权威判据，翻成业务错误
            raise BusinessError('username or email already exists') from exc
    return user_id


def update_display_name(user_id: int, display_name: str) -> int:
    with db.connect() as conn:
        row_count = repository.update_display_name(conn, user_id, display_name)
        conn.commit()
    if row_count == 0:
        raise BusinessError('user not found')
    return row_count


def delete_user(user_id: int) -> int:
    with db.connect() as conn:
        row_count = repository.delete_user(conn, user_id)
        conn.commit()
    if row_count == 0:
        raise BusinessError('user not found')
    return row_count
