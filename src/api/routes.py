from fastapi import APIRouter, Depends, Request

from src.api.schemas import GayOfTheDay, HTTPError, UserStatistics
from src.api.security import require_api_key
from src.db import create_new_user, find_gay, find_user, switch_user_orientation
from src.utils import calc_duration

router = APIRouter()


@router.get(
    "/statistics",
    status_code=200,
    name="Get users statistics",
    description="Statistics of all users that are stored in database.",
    responses={
        200: {"description": "OK.", "model": list[UserStatistics]},
        401: {"description": "Unauthorized.", "model": HTTPError},
        500: {"description": "Internal server error.", "model": HTTPError},
    },
    dependencies=[Depends(require_api_key)],
)
async def get_stat(
    request: Request, user_id: str | None = None, server_id: str | None = None
) -> list[UserStatistics]:
    collection = request.app.state.db.users
    query = {}
    if user_id:
        query.update({"user_id": user_id})
    if server_id:
        query.update({"server_id": server_id})
    users = await collection.find(query, {"_id": False}).to_list(length=1000)
    print(users)
    return [
        UserStatistics(
            user_id=user["user_id"],
            server_id=user["server_id"],
            duration=calc_duration(user["duration"], user["assignment_time"]),
            times=user["times"],
            is_gay=user["is_gay"],
        )
        for user in users
    ]


@router.post(
    "/gayoftheday",
    status_code=201,
    name="Set gay of the day",
    description="Set current gay of the day for proper calculation of statistics.",
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

    prev_gay = await find_gay(collection, gay.server_id)
    if prev_gay:
        await switch_user_orientation(collection, prev_gay.user_id, prev_gay.server_id)

    curr_gay = await find_user(collection, gay.user_id, gay.server_id)
    if not curr_gay:
        curr_gay = await create_new_user(collection, gay.user_id, gay.server_id)
    await switch_user_orientation(collection, gay.user_id, gay.server_id)

    curr_gay = await find_user(collection, gay.user_id, gay.server_id)

    return UserStatistics(**curr_gay.dict())
