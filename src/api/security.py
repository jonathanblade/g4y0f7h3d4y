from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from src.settings import SETTINGS


class CustomAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str:
        api_key: str = request.headers.get(self.model.name)
        if not api_key:
            raise HTTPException(
                detail="Missing API KEY.", status_code=status.HTTP_401_UNAUTHORIZED
            )
        return api_key


def require_api_key(
    api_key: str = Depends(CustomAPIKeyHeader(name="X-API-KEY")),
) -> None:
    if api_key != SETTINGS.api_key:
        raise HTTPException(
            detail="Invalid API KEY.", status_code=status.HTTP_401_UNAUTHORIZED
        )
