from pydantic import BaseModel

from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
