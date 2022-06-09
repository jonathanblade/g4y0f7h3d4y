from pydantic import BaseModel, Field


class HTTPError(BaseModel):
    detail: str = Field(description="Error detail.", example="Something went wrong.")


class UserStatistics(BaseModel):
    user_id: str = Field(description="User ID.", example="199469501362733056")
    server_id: str = Field(description="Server ID.", example="969761588238241802")
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
    user_id: str = Field(description="User ID.", example="199469501362733056")
    server_id: str = Field(description="Server ID.", example="969761588238241802")
