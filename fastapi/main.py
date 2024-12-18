import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from passlib.context import CryptContext
# from passlib.hash import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from api.routes.shift import router as shift_router

app = FastAPI(title="シフト管理API")


# SECRET_KEY = os.environ.get("SECRET_KEY")
# ALGORITHM = os.environ.get("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=10, deprecated="auto")
# pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=10, deprecated="auto")

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


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def authenticate_user(staff_id: str, password: str):
#     user = users_collection.find_one({"staff_id": staff_id})
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         staff_id: str = payload.get("sub")
#         if staff_id is None:
#             raise credentials_exception
#         token_data = TokenData(staff_id=staff_id)
#     except JWTError:
#         raise credentials_exception
    
#     user = users_collection.find_one({"staff_id": token_data.staff_id})
#     if user is None:
#         raise credentials_exception
#     return user


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