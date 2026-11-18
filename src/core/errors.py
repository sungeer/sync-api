from loguru import logger

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
    async def business_error(exc):
        logger.warning(
            'business error, method={}, path={}, msg={}',
            request.method, request.url.path, exc.msg,
        )
        # 业务拒绝是唯一允许 200 的失败场景
        return fail(exc.msg, http_status=200)


    # 入参错误 400
    @app.errorhandler(ParamError)
    async def param_error(exc):
        logger.warning(
            'param error, method={}, path={}, msg={}',
            request.method, request.url.path, exc.msg,
        )
        return fail(exc.msg, http_status=400)


    # 上游依赖不可用 503
    @app.errorhandler(UpstreamUnavailableError)
    async def upstream_unavailable(exc):
        logger.exception(
            'upstream unavailable, path={}',
            request.url.path
        )
        return fail(exc.msg, http_status=503)


    # 未登录 401
    @app.errorhandler(UnauthorizedError)
    async def unauthorized_error(exc):
        logger.warning(
            'unauthorized, method={}, path={}, msg={}',
            request.method, request.url.path, exc.msg,
        )
        return fail(exc.msg, http_status=401)


    # 无权限 403
    @app.errorhandler(ForbiddenError)
    async def forbidden_error(exc):
        return fail(exc.msg, http_status=403)


    # 路由匹配不到
    @app.errorhandler(404)
    async def not_found(exc):
        return fail(exc.detail, http_status=404)


    # 方法不对
    @app.errorhandler(405)
    async def method_not_allowed(exc):
        return fail(exc.detail, http_status=405)


    # 内部错误 500
    @app.errorhandler(Exception)
    async def server_error(exc):
        """兜底处理
        数据库崩了 依赖超时 等 系统级异常
        监控在这里感知
        """
        logger.exception(
            'unhandled server error path={}',
            request.url.path
        )
        return fail('internal server error', http_status=500)
