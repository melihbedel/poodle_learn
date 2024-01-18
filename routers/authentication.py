from fastapi import APIRouter, Query, Form
from models.user_data import UserData
from services.authenticaion import authentication_service



register_router = APIRouter(prefix='/register', tags=['Authentication'])

@register_router.post('', status_code=200)
def register(
    data: UserData,
    type: str = Query(enum=["teacher", "student"])
):
    
    authentication_service.register(data, type)



login_router = APIRouter(prefix='/login', tags=['Authentication'])

@login_router.post('', status_code=200)
def login(
    data: UserData,
    type: str = Query(enum=["teacher", "student"])
):
    pass