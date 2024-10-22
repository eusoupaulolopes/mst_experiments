from fastapi import APIRouter
from .endpoints import sensor

api_router = APIRouter()
api_router.include_router(sensor.router, tags=["sensor"])