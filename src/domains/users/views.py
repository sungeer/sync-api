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


def list_users():
    data = validate.require_body(request)  # dict

    limit = validate.optional_int(data, 'limit', 20)

    users = service.list_users(limit)
    logger.info('list users limit={} count={}', limit, len(users))
    return ok(data=users)


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


def update_display_name():
    data = validate.require_body(request)  # dict

    user_id = validate.require_int(data, 'user_id')
    display_name = validate.require_str(data, 'display_name')

    service.update_display_name(user_id, display_name)
    return ok()


def delete_user():
    data = validate.require_body(request)  # dict

    user_id = validate.require_int(data, 'user_id')
    service.delete_user(user_id)
    return ok()
