from datetime import datetime

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel

from src.settings import SETTINGS
from src.utils import calc_duration


def connect_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(SETTINGS.db_url)
    return client[SETTINGS.db_name]


class User(BaseModel):
    user_id: int
    duration: int
    times: int
    assignment_time: datetime | None
    is_gay: bool


async def create_new_user(collection: AsyncIOMotorCollection, user_id: int) -> None:
    user = User(
        user_id=user_id,
        duration=0,
        times=0,
        assignment_time=None,
        is_gay=False,
    )
    await collection.insert_one(user.dict())


async def find_user_by_id(
    collection: AsyncIOMotorCollection, user_id: int
) -> User | None:
    user = await collection.find_one({"user_id": user_id}, {"_id": False})
    if user:
        return User(**user)
    return user


async def find_gay(collection: AsyncIOMotorCollection) -> User | None:
    user = await collection.find_one({"is_gay": True}, {"_id": False})
    if user:
        return User(**user)
    return user


async def switch_user_orientation(
    collection: AsyncIOMotorCollection, user_id: int
) -> None:
    user = await find_user_by_id(collection, user_id)
    if user:
        await collection.update_one(
            {"user_id": user.user_id},
            {
                "$set": {
                    "duration": calc_duration(user.duration, user.assignment_time),
                    "times": user.times if user.is_gay else user.times + 1,
                    "assignment_time": None if user.is_gay else datetime.utcnow(),
                    "is_gay": False if user.is_gay else True,
                }
            },
        )
