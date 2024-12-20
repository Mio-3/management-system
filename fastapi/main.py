import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from api.routes.shift import router as shift_router
from api.routes.auth import router as auth_router

app = FastAPI(title="シフト管理API")


origins = [
  "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://db:27017")
    app.mongodb_client = AsyncIOMotorClient(
        mongodb_url,
        server_api=ServerApi('1')
    )
    app.mongodb = app.mongodb_client.management_system
    app.collection_shifts = app.mongodb.shifts
    
    shift_router.app = app
    
    try:
        await app.mongodb_client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/health")
async def health_check():
    try:
        await app.mongodb_client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "message": "MongoDB connection is active"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection error: {str(e)}"
        )


app.include_router(shift_router, prefix="/api/shifts", tags=["shifts"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])