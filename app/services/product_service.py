from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.models import Product
from app.serializers import schemas


class ProductService:
    async def get_all_products(
        self, db: AsyncSession, offset: int, limit: int, order_by: str = "id"
    ) -> List[schemas.Product]:
        if order_by == "price":
            return await crud.get_all_products_sorted_by_price(
                db=db, offset=offset, limit=limit
            )
        else:
            return await crud.get_all_products(
                db=db, offset=offset, limit=limit
            )

    async def get_product_by_id(
        self, db: AsyncSession, product_id: int
    ) -> Optional[schemas.Product]:
        return await crud.get_product_by_id(db=db, product_id=product_id)

    async def create_product(
        self, db: AsyncSession, product: schemas.ProductCreate
    ) -> schemas.Product:
        return await crud.create_product(db=db, product=product)

    async def update_product(
        self, db: AsyncSession, product_id: int, product: schemas.ProductUpdate
    ) -> Optional[schemas.Product]:
        return await crud.update_product(
            db=db, product_id=product_id, product=product
        )

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        return await crud.delete_product(db=db, product_id=product_id)

    async def delete_all_products(self, db: AsyncSession):
        await db.query(Product).delete()
        await db.commit()


class ProductValidator:
    def validate_product_create(self, product: schemas.ProductCreate):
        if product.price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")

    def validate_product_update(self, product: schemas.ProductUpdate):
        if product.price and product.price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")
