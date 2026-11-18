from contextlib import suppress

import httpx2

HTTPError = httpx2.HTTPError

Timeout = httpx2.Timeout


class _ClientHolder:

    def __init__(self):
        self._client = None

    def init(self):
        self._client = httpx2.Client(
            timeout=httpx2.Timeout(
                connect=5.0,  # 连接阶段快速失败
                read=30.0,  # 给服务端留足处理时间
                write=5.0,  # 发送请求体
                pool=5.0  # 池排队超时
            ),
            limits=httpx2.Limits(
                max_connections=100,
                keepalive_expiry=0.0,
            ),
            verify=False,
        )

    def get_client(self):
        if self._client is None:
            raise RuntimeError('HTTP client not initialized')
        return self._client

    def close(self):
        if self._client is not None:
            with suppress(Exception):
                self._client.close()
            self._client = None


http = _ClientHolder()
