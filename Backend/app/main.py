from fastapi import FastAPI
from app.api.routes import auth, users, items, media  # ajusta según tus módulos

app = FastAPI(title="Testimonial CMS")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(media.router, prefix="/media", tags=["Media"])

@app.get("/")
def root():
    return {"message": "API funcionando!"}