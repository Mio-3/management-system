import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta
import pytz

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SESSION_ID_LENGTH = 64
SESSION_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_session_id() -> str:
    return secrets.token_urlsafe(SESSION_ID_LENGTH)


def get_session_expiry() -> datetime:
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    return now + timedelta(minutes=SESSION_EXPIRE_MINUTES)