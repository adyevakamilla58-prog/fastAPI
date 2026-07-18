from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.users import router as users_router

app = FastAPI(
    title="API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router, tags=["Users"])

@app.get("/")
async def root():
    return {"message": "работает"}

@app.get("/health")
async def health():
    return {"status": "ok", "database": "sqlite"}

@app.get("/test-user")
async def test_user_route():
    return {"message": "Ура, тестовый роут пользователя работает прямо из main!"}