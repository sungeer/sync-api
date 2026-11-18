from src import settings
from src.core.response import ok


def liveness():
    data = {
        'env': settings.ENVIRONMENT,
        'version': settings.VERSION,
    }
    return ok(data)
