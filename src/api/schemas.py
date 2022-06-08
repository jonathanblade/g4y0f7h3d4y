from pydantic import BaseModel, Field


class HTTPError(BaseModel):
    detail: str = Field(description="Error detail.", example="Something went wrong.")


class UserStatistics(BaseModel):
    user_id: int = Field(description="User ID.", example=12345)
    duration: int = Field(
        description="Total time in seconds how long the user has been a gay of the day.",
        example=12345,
    )
    times: int = Field(
        description="Total number of times the user has been a gay of the day.",
        example=12345,
    )
    is_gay: bool = Field(
        description="Flag which describing the user is gay of the day or not.",
        example=True,
    )


class GayOfTheDay(BaseModel):
    user_id: int = Field(description="User ID.", example=12345)
