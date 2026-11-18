from flask import request
from loguru import logger
from werkzeug.exceptions import HTTPException

from src.utils.exceptions import (
    BusinessError,
    ParamError,
    UpstreamUnavailableError,
    UnauthorizedError,
    ForbiddenError
)
from src.core.response import fail


def register_errors(app):
    # 业务失败
    @app.errorhandler(BusinessError)
    def business_error(exc):
        logger.warning(
            'business error, method={}, path={}, msg={}',
            request.method, request.path, exc.msg,
        )
        # 业务拒绝是唯一允许 200 的失败场景
        return fail(exc.msg, http_status=200)


    # 入参错误 400
    @app.errorhandler(ParamError)
    def param_error(exc):
        logger.warning(
            'param error, method={}, path={}, msg={}',
            request.method, request.path, exc.msg,
        )
        return fail(exc.msg, http_status=400)


    # 上游依赖不可用 503
    @app.errorhandler(UpstreamUnavailableError)
    def upstream_unavailable(exc):
        logger.exception(
            'upstream unavailable, path={}',
            request.path
        )
        return fail(exc.msg, http_status=503)


    # 未登录 401
    @app.errorhandler(UnauthorizedError)
    def unauthorized_error(exc):
        logger.warning(
            'unauthorized, method={}, path={}, msg={}',
            request.method, request.path, exc.msg,
        )
        return fail(exc.msg, http_status=401)


    # 无权限 403
    @app.errorhandler(ForbiddenError)
    def forbidden_error(exc):
        return fail(exc.msg, http_status=403)


    # 路由匹配不到
    @app.errorhandler(404)
    def not_found(exc):
        return fail(exc.description, http_status=404)


    # 方法不对
    @app.errorhandler(405)
    def method_not_allowed(exc):
        return fail(exc.description, http_status=405)


    # 框架抛的其他 HTTP 异常 413 请求体过大 415 类型不支持
    @app.errorhandler(HTTPException)
    def http_error(exc):
        logger.info(
            'http error, method={}, path={}, status={}',
            request.method, request.path, exc.code,
        )
        return fail(exc.description, http_status=exc.code)


    # 内部错误 500
    @app.errorhandler(Exception)
    def server_error(exc):  # noqa
        """兜底处理
        数据库崩了 依赖超时 等 系统级异常
        监控在这里感知
        """
        logger.exception(
            'unhandled server error path={}',
            request.path
        )
        return fail('internal server error', http_status=500)
