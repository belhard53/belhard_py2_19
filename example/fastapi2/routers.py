from fastapi import APIRouter, HTTPException, Depends, Query

from schemas import *
from database import UserRepository as ur
from models import UserFilter

# pip install fastapi_filter
from fastapi_filter import FilterDepends

default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags = ["Пользователи"]
)

quizes_router = APIRouter(
    prefix="/quizes",
    tags = ["Квизы"]
)



@default_router.get('/', tags=['API V1'])
async def index():    
    return {'data':'ok'}



# ответ в виде одиночного списка
@users_router.get('')
async def users_get(
            limit:int = Query(ge=1, lt=10, default=3), 
            offset:int = Query(ge=0, default=0),            
            user_filter: UserFilter = FilterDepends(UserFilter)
        ) -> dict[str, int | list[User]]: 
     
    # users =   await ur.get_users(limit, offset, user_filter)
    users =   await ur.get_users(limit, offset, user_filter)
    
    # return users
    
    # с развернутым ответом 
    return {"data":users, "limit":limit, "offset":offset}


@users_router.get('/u2')
async def users_get2() -> dict[str, list[User] | str]: 
    users =   await ur.get_users()
    return {'status':'ok', 'data':users}


@users_router.get('/{id}')
async def user_get(id: int) -> User :  
    user =   await ur.get_user(id)
    if user:
        return user    
    raise HTTPException(status_code=404, detail="User not found")
    # или return {'err':"User not found, ..."} # но тогда get_user(id) -> User | dict[str,str]
    
    
@users_router.post('')
async def add_user(user:UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}    


@quizes_router.get('')
def index():
    return {'data':'quizes'}



# пример развернутого ответа
#     {
            # "items": [...],
            # "total": 100,
            # "page": 1,
            # "size": 10,
            # "pages": 10
            # }

            # Или с ссылками:

            # {
            # "items": [...],
            # "total": 100,
            # "page": 1,
            # "size": 10,
            # "pages": 10,
            # "links": {
            # "next": "http://api.example.com/items?page=2",
            # "prev": null,
            # "first": "http://api.example.com/items?page=1",
            # "last": "http://api.example.com/items?page=10"
            # }
            # }