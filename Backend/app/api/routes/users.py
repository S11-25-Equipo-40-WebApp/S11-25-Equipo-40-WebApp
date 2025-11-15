from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return [{"id": 1, "name": "User Demo"}]

@router.post("/")
def create_user():
    return {"message": "user created"}