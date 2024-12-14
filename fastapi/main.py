import os
import strawberry
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from pymongo import MongoClient
from typing import Optional
from passlib.context import CryptContext
from passlib.hash import bcrypt
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from models import ShiftCreate, Shift, UserResponse, LoginRequest, TokenData
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN")


client = MongoClient(os.environ.get("MONGO_URL"))
db = client['management_system']
shift_collection = db['shifts']
users_collection = db['users']


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=10, deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=10, deprecated="auto")

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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(staff_id: str, password: str):
    user = users_collection.find_one({"staff_id": staff_id})
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        staff_id: str = payload.get("sub")
        if staff_id is None:
            raise credentials_exception
        token_data = TokenData(staff_id=staff_id)
    except JWTError:
        raise credentials_exception
    
    user = users_collection.find_one({"staff_id": token_data.staff_id})
    if user is None:
        raise credentials_exception
    return user

@app.post("/shifts/", response_model=Shift)
async def create_shift(shift: ShiftCreate, user: UserResponse = Depends(get_current_user)):