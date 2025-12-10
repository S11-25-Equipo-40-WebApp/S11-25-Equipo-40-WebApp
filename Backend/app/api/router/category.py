from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.schemas import CategoryResponse
from app.services.category import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("", status_code=status.HTTP_200_OK)
def get_categories(db: SessionDep):
    """Retrieve all categories.

    Args:
    - db (SessionDep): database session

    Returns:
    - list[CategoryResponse]: list of all categories
    """

    categories = CategoryService.get_all_categories(db)
    return [CategoryResponse.model_validate(cat) for cat in categories]
