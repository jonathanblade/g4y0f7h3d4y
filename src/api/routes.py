from fastapi import APIRouter, Depends, Request

from src.api.schemas import GayOfTheDay, HTTPError, UserStatistics
from src.api.security import require_api_key
from src.db import create_new_user, find_gay, find_user_by_id, switch_user_orientation
from src.utils import calc_duration

router = APIRouter()


@router.get(
    "/statistics",
    status_code=200,
    name="Get users statistics.",
    responses={
        200: {"description": "OK.", "model": list[UserStatistics]},
        401: {"description": "Unauthorized.", "model": HTTPError},
        500: {"description": "Internal server error.", "model": HTTPError},
    },
    dependencies=[Depends(require_api_key)],
)
async def get_stat(request: Request) -> list[UserStatistics]:
    collection = request.app.state.db.users
    users = await collection.find({}, {"_id": False}).to_list(length=100)
    return [
        UserStatistics(
            user_id=user["user_id"],
            duration=calc_duration(user["duration"], user["assignment_time"]),
            times=user["times"],
            is_gay=user["is_gay"],
        )
        for user in users
    ]


@router.post(
    "/gayoftheday",
    status_code=201,
    name="Set gay of the day.",
    responses={
        201: {"description": "Created.", "model": UserStatistics},
        400: {"description": "Bad request.", "model": HTTPError},
        401: {"description": "Unauthorized.", "model": HTTPError},
        500: {"description": "Internal server error.", "model": HTTPError},
    },
    dependencies=[Depends(require_api_key)],
)
async def set_curr_gay(request: Request, gay: GayOfTheDay) -> UserStatistics:
    collection = request.app.state.db.users

    prev_gay = await find_gay(collection)
    if prev_gay:
        await switch_user_orientation(collection, prev_gay.user_id)

    curr_gay = await find_user_by_id(collection, gay.user_id)
    if not curr_gay:
        curr_gay = await create_new_user(collection, gay.user_id)
    await switch_user_orientation(collection, gay.user_id)

    curr_gay = await find_user_by_id(collection, gay.user_id)

    return UserStatistics(**curr_gay.dict())
