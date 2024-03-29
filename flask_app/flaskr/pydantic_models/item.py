from pydantic import BaseModel
from typing import List, Optional


class CreateItem(BaseModel):
    class Model(BaseModel):
        size: int
        price: int
        rooms: int
        floor: int
        total_floor: int
        type: str
        city: str
        address: str
        description: str
        images_id: List[int]

    data: Model


class PatchItem(BaseModel):
    class Model(BaseModel):
        size: Optional[int]
        price: Optional[int]
        rooms: Optional[int]
        floor: Optional[int]
        total_floor: Optional[int]
        type: Optional[str]
        city: Optional[str]
        address: Optional[str]
        description: Optional[str]
        images_id: Optional[List[int]]

    data: Model


class Image(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True


class _Item(BaseModel):
    id: int
    size: int
    price: int
    rooms: int
    floor: int
    total_floor: int
    type: str
    city: str
    address: str
    description: str
    images_id: List[int]
    images: List[Image]
    user_id: int

    class Config:
        orm_mode = True


class DumpItem(BaseModel):
    data: _Item


class DumpItemsList(BaseModel):
    data: List[_Item]
    total: int
