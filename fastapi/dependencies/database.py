from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from fastapi import Request, Depends


async def get_database(request: Request) -> AsyncIOMotorClient:
    return request.app.mongodb_client


async def get_users_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.mongodb.users


async def get_sessions_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.mongodb.sessions


async def get_shifts_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.mongodb.shifts