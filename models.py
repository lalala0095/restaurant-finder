from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str

class RestaurantObject(BaseModel):
    id: str
    name: str
    address: str
    cuisine: str
    rating: str
    price_level: str
    operating_hours: str