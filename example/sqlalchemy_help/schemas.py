from pydantic import BaseModel


class PhoneNumberSchema(BaseModel):    
    phone_type: str
    number: str
    
    
class UserSchema(BaseModel):    
    fname: str
    lname: str
    gender: str
    age: int    
    phones: list[PhoneNumberSchema] = []


