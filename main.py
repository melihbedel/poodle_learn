from fastapi import FastAPI
from routers.authentication import register_router, login_router

app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)