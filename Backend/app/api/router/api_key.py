from uuid import UUID

from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.core.deps import AdminDep
from app.schemas import APIKeyCreate, APIKeyListResponse, APIKeyResponse
from app.services.api_keys import APIKeyService
from app.services.user import UserService

router = APIRouter(
    prefix="/api-keys",
    tags=["api-keys"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=APIKeyResponse)
async def api_keys_create(data: APIKeyCreate, db: SessionDep, current_user: AdminDep):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return APIKeyService.create_api_key(db, tenant_owner_id, data.name)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[APIKeyListResponse])
async def api_keys_list(db: SessionDep, current_user: AdminDep):
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return APIKeyService.list_api_keys(db, tenant_owner_id)


@router.post("/revoke/{api_key_id}", status_code=status.HTTP_200_OK)
async def api_keys_revoke(api_key_id: UUID, db: SessionDep, current_user: AdminDep) -> bool:
    tenant_owner_id = UserService._get_tenant_owner_id(current_user)
    return APIKeyService.revoke_api_key(db, api_key_id, tenant_owner_id)
