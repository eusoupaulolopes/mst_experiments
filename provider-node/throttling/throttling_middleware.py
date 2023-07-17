from typing import Optional
from fastapi import Request, Response
from fastapi.exceptions import HTTPException
from ratelimit import limits, RateLimitException

limiter = limits(
    calls=50,
    period=10
)

async def throttling_middleware(request: Request, call_next):
    try:
        await limiter.consume(request.client.host)
    except RateLimitException as exc:
        raise HTTPException(status_code=429, detail=str(exc))
    return await call_next(request)
