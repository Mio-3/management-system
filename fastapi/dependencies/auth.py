from fastapi import Depends, HTTPException, Cookie
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from api.routes.auth import get_users_collection
import pytz


async def get_current_user(
  session_id: str = Cookie(None),
  db: AsyncIOMotorClient = Depends(get_users_collection)
):
    if not session_id:
        raise HTTPException(status_code=401, detail="ログインが必要です")
    
    session = await db.sessions.find_one({
      "session_id": session_id,
      "expires_at": {"$gte": datetime.now(pytz.timezone("Asia/Tokyo"))}
    })
    if not session:
        raise HTTPException(status_code=401, detail="セッションが有効切れです")

    user = await db.users.find_one({"staff_id": session["staff_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    return user