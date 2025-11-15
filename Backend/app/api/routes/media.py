from fastapi import APIRouter

router = APIRouter()

@router.get("/cloudinary")
def test_cloudinary():
    return {"message": "cloudinary ok"}

@router.get("/youtube")
def test_youtube():
    return {"message": "youtube ok"}