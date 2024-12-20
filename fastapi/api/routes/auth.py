from fastapi import APIRouter, HTTPException, Response, Cookie
from fastapi import Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from utils.auth import verify_password, create_session_id, get_session_expiry, get_password_hash
from dependencies.database import get_users_collection, get_sessions_collection
from models.users import UserCreate
from models.auth import LoginRequest

router = APIRouter()


@router.post("/login/")
async def login(
  request: Request,
  response: Response,
  login_data: LoginRequest,
  users: AsyncIOMotorClient = Depends(get_users_collection),
  db: AsyncIOMotorClient = Depends(get_sessions_collection)
):
    user = await users.find_one({"staff_id": login_data.staff_id})
    if not user or not verify_password(
      login_data.password,
      user["hashed_password"]
    ):
        raise HTTPException(status_code=401, detail="スタッフIDかパスワードが間違っています")
    
    session_id = create_session_id()
    expires = get_session_expiry()
    
    await db.sessions.insert_one({
        "session_id": session_id,
        "staff_id": login_data.staff_id,
        "expires_at": expires
    })

    response.set_cookie(
      key="session_id",
      value=session_id,
      expires=expires,
      httponly=True,  # 重要
      secure=True,
      samesite="strict"
    )
    
    return {"message": "ログインしました"}


@router.post("/logout/")
async def logout(
  response: Response,
  session_id: str = Cookie(None),
  sessions: AsyncIOMotorClient = Depends(get_sessions_collection)
):
    if not session_id:
        raise HTTPException(status_code=401, detail="ログインが必要です")

    result = await sessions.delete_one({"session_id": session_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="無効なセッションです")

    response.delete_cookie(
        key="session_id",
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {"message": "ログアウトしました"}


@router.post("/register/")
async def register_user(
  user_data: UserCreate,
  users: AsyncIOMotorCollection = Depends(get_users_collection)
):
    if await users.find_one({"staff_id": user_data.staff_id}):
        raise HTTPException(
          status_code=400,
          detail="このスタッフIDは既に登録されています"
        )

    hashed_password = get_password_hash(user_data.password)
    
    user_dict = {
      "staff_id": user_data.staff_id,
      "name": user_data.name,
      "hashed_password": hashed_password,
      "role": user_data.role,
      "is_active": True
    }
    
    await users.insert_one(user_dict)
    return {"message": "ユーザーの登録が完了しました"}


@router.delete("/users/all/", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_all_users(
  users: AsyncIOMotorCollection = Depends(get_users_collection),
  sessions: AsyncIOMotorCollection = Depends(get_sessions_collection)
):
    try:
        users_result = await users.delete_many({})
        sessions_result = await sessions.delete_many({})
        
        return {
          "message": "全てのユーザーとセッションを削除しました",
          "deleted_users": users_result.deleted_count,
          "deleted_sessions": sessions_result.deleted_count
        }
    except Exception as e:
        raise HTTPException(
          status_code=500,
          detail=f"削除中にエラーが発生しました: {str(e)}"
        )


@router.delete("/user/", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_user(
  staff_id: str,
  users: AsyncIOMotorCollection = Depends(get_users_collection),
  sessions: AsyncIOMotorCollection = Depends(get_sessions_collection)
):
    try:
        user_result = await users.delete_one({"staff_id": staff_id})
        session_result = await sessions.delete_many({"staff_id": staff_id})
        
        return {
          "message": f"ユーザー {staff_id} を削除しました",
          "deleted_user": user_result.deleted_count,
          "deleted_sessions": session_result.deleted_count
        }
    except Exception as e:
        raise HTTPException(
          status_code=500,
          detail=f"削除中にエラーが発生しました: {str(e)}"
        )