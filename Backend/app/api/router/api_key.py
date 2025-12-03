from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.db import SessionDep
from app.core.deps import get_current_user, require_admin
from app.schemas import APIKeyCreate, APIKeyListResponse, APIKeyResponse
from app.services.api_keys import create_api_key, list_api_keys, revoke_api_key

router = APIRouter(
    prefix="/api-keys",
    tags=["api-keys"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=APIKeyResponse)
async def api_keys_create(data: APIKeyCreate, db: SessionDep):
    return create_api_key(db, data.name)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[APIKeyListResponse])
async def api_keys_list(db: SessionDep):
    return list_api_keys(db)


@router.post(
    "/revoke/{api_key_id}", dependencies=[Depends(require_admin)], status_code=status.HTTP_200_OK
)
async def api_keys_revoke(api_key_id: UUID, db: SessionDep) -> bool:
    return revoke_api_key(db, api_key_id)
