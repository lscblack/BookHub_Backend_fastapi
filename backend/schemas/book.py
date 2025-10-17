from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookOut(BookBase):
    id: int
        # ✅ Correct config for Pydantic v2
    model_config = {
        "from_attributes": True
    }


class Config:
    orm_mode = True