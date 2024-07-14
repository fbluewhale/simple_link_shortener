from typing import AsyncIterable
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import uuid
import json
import logging
from logging.handlers import RotatingFileHandler
from src.schemas.general.log import LogBase, RequestLog, ResponseLog
from starlette.types import Message


class AsyncIteratorWrapper:
    """The following is a utility class that transforms a
    regular iterable to an asynchronous one.

    link: https://www.python.org/dev/peps/pep-0492/#example-2
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


class LoggingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, *, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        tracking_number = str(uuid.uuid4())

        # await self.set_body(request)

        # Create the request log object
        req_data = (
            await request.json()
            if (
                request.headers.get("Content-Type") == "application/json"
                and int(request.headers.get("content-length", 0)) > 0
            )
            else {}
        )
        request_log = RequestLog(
            req_method=request.method,
            req_url=str(request.url),
            req_data=req_data,
            client_ip=request.client.host,
            user_id="Extracted User ID",
            username="Extracted Username",
        )

        response = await call_next(request)
        duration = time.time() - start_time
        # Create the response log object
        if response:
            resp_body = [
                section async for section in response.__dict__["body_iterator"]
            ]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

            try:
                resp_body = str(resp_body[0].decode())
            except:
                resp_body = str(resp_body)

        response_log = ResponseLog(
            res_status_code=response.status_code,
            duration=duration,
            res_data=((
                (json.loads(resp_body) if response else dict())
                if "application/json" in response.headers.get("content-type")
                else dict(data=resp_body)
            ) if response.status_code <300 else dict() ),
        )

        # Create the complete log entry
        log_entry = LogBase(
            application_ip="127.0.0.1",
            browser=request.headers.get("User-Agent", "Unknown Browser"),
            client_ip=request.client.host,
            tracking_number=tracking_number,
            req_data=request_log.dict(),
            req_method=request.method,
            req_time=request_log.req_time,
            req_url=str(request.url),
            res_data=response_log.dict(),
            res_status_code=response.status_code,
            res_time=response_log.res_time,
            duration=duration,
            user_id="Extracted User ID",
            username="Extracted Username",
        )
        self._logger.info(log_entry.json())

        return response
