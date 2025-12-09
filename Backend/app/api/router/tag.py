from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.schemas.tag import TagResponse
from app.services.tag import TagService

router = APIRouter(
    prefix="/tags",
    tags=["Tag"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_tags(db: SessionDep):
    """Get all tags.

    Returns:
    - list[TagResponse]: list of all tags
    """
    tags = TagService.get_all_tags(db)
    return [TagResponse.model_validate(tag) for tag in tags]
