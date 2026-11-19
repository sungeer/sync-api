from sqlalchemy.exc import IntegrityError

from src.utils.exceptions import BusinessError, ParamError
from src.core.db import db
from src.domains.users import models


def get_user(user_id: int) -> dict:
    with db.connect() as conn:
        user = models.query_one(conn, user_id)
    if user is None:
        raise BusinessError('user not found')
    return user


def get_user_by_username(username: str) -> dict:
    with db.connect() as conn:
        user = models.query_one_by_username(conn, username)
    if user is None:
        raise BusinessError('user not found')
    return user


def get_user_by_email(email: str) -> dict:
    with db.connect() as conn:
        user = models.query_one_by_email(conn, email)
    if user is None:
        raise BusinessError('user not found')
    return user


def list_users(limit: int, offset: int) -> list[dict]:
    with db.connect() as conn:
        users = models.query_many(conn, limit, offset)
    return users


def count_users() -> int:
    with db.connect() as conn:
        total = models.count_all(conn)
    return total


def create_user(username: str, display_name: str | None, email: str) -> int:
    try:
        with db.begin() as conn:
            if models.username_exists(conn, username):
                raise BusinessError('username already exists')
            if models.email_exists(conn, email):
                raise BusinessError('email already exists')
            user_id = models.insert_user(conn, username, display_name, email)
    except IntegrityError as exc:
        # 预检漏网的竞态：唯一键是权威判据，翻成业务错误
        raise BusinessError('username or email already exists') from exc
    return user_id


def update_user(user_id: int, display_name: str | None, email: str | None) -> dict:
    if display_name is None and email is None:
        raise ParamError('display_name or email is required')
    try:
        with db.begin() as conn:
            # 先确认存在：UPDATE 的 rowcount 在新旧值相同时为 0，不能当判据
            if models.query_one(conn, user_id) is None:
                raise BusinessError('user not found')
            models.update_user(conn, user_id, display_name, email)
            user = models.query_one(conn, user_id)
    except IntegrityError as exc:
        raise BusinessError('email already exists') from exc
    return user


def delete_user(user_id: int) -> int:
    with db.begin() as conn:
        row_count = models.delete_user(conn, user_id)
    if row_count == 0:
        raise BusinessError('user not found')
    return row_count
