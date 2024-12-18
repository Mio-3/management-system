from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from datetime import datetime
from bson import ObjectId
from models.schemas import ShiftPost, ShiftPostDB
import pytz

router = APIRouter()


async def get_collection() -> AsyncIOMotorCollection:
    return router.app.collection_shifts


@router.post("/post/", response_model=ShiftPostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: ShiftPost, collection: AsyncIOMotorCollection = Depends(get_collection)):
    post_dict = post.dict()

    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    utc_now = now.astimezone(pytz.UTC)
    
    post_dict["created_at"] = utc_now

    result = await collection.insert_one(post_dict)
    created_post = await collection.find_one({"_id": result.inserted_id})
    if created_post is None:
        raise HTTPException(status_code=404, detail="Created post not found")

    return created_post


@router.get("/posts/", response_model=List[ShiftPostDB], status_code=status.HTTP_200_OK)
async def get_shift_posts(
    collection: AsyncIOMotorCollection = Depends(get_collection)
):
    try:
        posts = await collection.find().to_list(length=None)
        for post in posts:
            if 'created_at' not in post:
                post['created_at'] = datetime.now(pytz.timezone('Asia/Tokyo'))
        
        print(f"Found {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))




