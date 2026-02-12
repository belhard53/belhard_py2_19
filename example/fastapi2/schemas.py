from pydantic import BaseModel, ConfigDict

class UserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None
    
class User(UserAdd):    
    id: int
    
    model_config = ConfigDict(from_attributes=True)    
    # возможность сбора модели из атрибутов объекта (как правило из ORM)
    # Без этого параметра Pydantic ожидал бы словарь, а не объект с атрибутами.
    
       
class UserId(BaseModel):
    id: int