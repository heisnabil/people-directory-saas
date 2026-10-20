"""
API router aggregation.

Mounts all route modules under the /api/v1 prefix.
Adding new resource routes only requires an import and include here.
"""

from fastapi import APIRouter

from app.api.routes import employees, health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(employees.router)
