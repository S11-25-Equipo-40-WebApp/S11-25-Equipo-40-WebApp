from fastapi import APIRouter

from app.schemas.auth import UserResponse

# from app.core.database import get_db
# from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register():
    return {"mensaje": "register!"}


"""def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))"""


@router.post("/login")
async def login():
    return {"mensaje": "login!"}


"""def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        token = AuthService.login_user(db, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))"""
