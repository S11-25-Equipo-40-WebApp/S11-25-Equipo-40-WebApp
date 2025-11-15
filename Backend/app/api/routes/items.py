from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_items():
    return [{"id": 1, "item": "Demo Item"}]

@router.post("/")
def create_item():
    return {"message": "item created"}