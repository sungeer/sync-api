import uuid


def hex_id(n: int = 18) -> str:
    return uuid.uuid4().hex[:n]
