from pydantic import BaseModel, ValidationError



class Tag(BaseModel):
    id: int
    tag: str



class City(BaseModel):
    city_id: int
    name: str
    population: int | None = None
    tags: list[Tag]

input_json = """
{
    "city_id": 12,
    "name": "Minsk",
    "population": 2000000,
    "tags": [
        {"id":1, "tag":"Capital"},
        {"id":2, "tag":"river"}
    ]
}
"""

try:
    city = City.model_validate_json(input_json)
    
    
except ValidationError as e:
    print(e.json())
else:
    print(1111, city)
    print(city.model_dump())  
      
    print(city.tags[1].tag)