# pip install uvicorn
# pip install fastapi

from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel


class User1(BaseModel):
    name: str
    age: int | None = None

app = FastAPI()

@app.get('/', tags=['Майн get'])
def home():
    return {"hello1": "python", "hello2": 'fastapi'}


@app.get('/users', tags=['usersGET'])
def users(f: str='123', q:str=None):
    return {"status": "success", "data": 'data1', 'f':f, 'q':q}


@app.post('/users', tags=['userPOST'])
def home_post(user: User1 = Depends()):
    print(user)    
    return {"status": "success post", "data": {'id':11111, 'add_user':f'{user.name} {user.age}'}}




if __name__ == '__main__':    
    uvicorn.run("main:app", reload=True)  
    
# uvicorn main:app --reload  
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload      