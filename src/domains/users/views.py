from flask import request
from loguru import logger

from src.core.response import ok
from src.domains.users import service
from src.utils import validate


def get_user():
    data = validate.require_body(request)  # dict

    user_id = validate.require_int(data, 'user_id')

    user = service.get_user(user_id)
    return ok(data=user)


def get_user_by_username():
    data = validate.require_body(request)  # dict

    username = validate.require_str(data, 'username')

    user = service.get_user_by_username(username)
    return ok(data=user)


def get_user_by_email():
    data = validate.require_body(request)  # dict

    email = validate.require_str(data, 'email')

    user = service.get_user_by_email(email)
    return ok(data=user)


def list_users():
    data = validate.require_body(request)  # dict

    limit = validate.optional_int(data, 'limit', 20)
    offset = validate.optional_int(data, 'offset', 0)

    users = service.list_users(limit, offset)
    logger.info(
        'list users, limit={}, offset={}, count={}',
        limit, offset, len(users)
    )
    return ok(data=users)


def count_users():
    validate.require_body(request)  # dict

    total = service.count_users()
    return ok(data={'total': total})


def create_user():
    data = validate.require_body(request)  # dict

    username = validate.require_str(data, 'username')
    display_name = validate.optional_str(data, 'display_name')
    email = validate.require_str(data, 'email')

    new_id = service.create_user(username, display_name, email)
    data = {
        'user_id': new_id
    }
    return ok(data=data)


def update_user():
    data = validate.require_body(request)  # dict

    user_id = validate.require_int(data, 'user_id')
    display_name = validate.optional_str(data, 'display_name')
    email = validate.optional_str(data, 'email')

    user = service.update_user(user_id, display_name, email)
    return ok(data=user)


def delete_user():
    data = validate.require_body(request)  # dict

    user_id = validate.require_int(data, 'user_id')

    service.delete_user(user_id)
    return ok()
