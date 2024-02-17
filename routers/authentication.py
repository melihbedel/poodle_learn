from fastapi import APIRouter, Query, HTTPException
from models.authentication import LoginData, RegisterData
from services.authenticaion import authentication_service, token_service



register_router = APIRouter(prefix='/register', tags=['Authentication'])

@register_router.post('', status_code=200)
def register(
    data: RegisterData,
    type: str = Query(enum=["teacher", "student"])
):
    if authentication_service.user_exists(data.email):
        raise HTTPException(status_code=400, detail='User already exists')
    
    return authentication_service.register(data, type)



login_router = APIRouter(prefix='/login', tags=['Authentication'])

@login_router.post('', status_code=200)
def login(
    data: LoginData,
    type: str = Query(enum=["teacher", "student"])
):
    user = authentication_service.login(data, type)

    if user:
        return f'Token: {token_service.create_jwt_token(token_service.create_payload(data, type))}'