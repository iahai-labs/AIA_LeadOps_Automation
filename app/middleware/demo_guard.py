from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.config import settings


class DemoGuardMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method != "POST" or request.url.path != "/api/v1/leads":
            return await call_next(request)

        client_ip = request.headers.get("x-real-ip")
        if not client_ip and request.client:
            client_ip = request.client.host
        client_ip = client_ip or "unknown"

        now = time.monotonic()
        window_start = now - 60
        bucket = self._requests[client_ip]

        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= max(1, settings.demo_rate_limit_per_minute):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Public demo rate limit reached. Please try again shortly."
                },
            )

        bucket.append(now)
        return await call_next(request)
