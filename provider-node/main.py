from typing import Union
from fastapi import FastAPI, Request
from api.v1.api import api_router
from configs import settings
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
# from throttling.throttling_middleware import throttling_middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
]

limiter = Limiter(key_func=get_remote_address)
    
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", middleware=middleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

Instrumentator().instrument(app).expose(app)

@app.get("/")
# @limiter.limit("10/minute")
def read_root(request: Request):
    return {"instance": settings.INSTANCE_ID}


