from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.models.models import Product
from app.serializers import schemas


class ProductService:
    def get_all_products(
        self, db: Session, offset: int, limit: int, order_by: str = "id"
    ) -> List[schemas.Product]:
        if order_by == "price":
            return crud.get_all_products_sorted_by_price(
                db=db, offset=offset, limit=limit
            )
        else:
            return crud.get_all_products(db=db, offset=offset, limit=limit)

    def get_product_by_id(
        self, db: Session, product_id: int
    ) -> Optional[schemas.Product]:
        return crud.get_product_by_id(db=db, product_id=product_id)

    def create_product(
        self, db: Session, product: schemas.ProductCreate
    ) -> schemas.Product:
        return crud.create_product(db=db, product=product)

    def update_product(
        self, db: Session, product_id: int, product: schemas.ProductUpdate
    ) -> Optional[schemas.Product]:
        return crud.update_product(
            db=db, product_id=product_id, product=product
        )

    def delete_product(self, db: Session, product_id: int) -> bool:
        return crud.delete_product(db=db, product_id=product_id)

    def delete_all_products(self, db: Session):
        db.query(Product).delete()
        db.commit()


class ProductValidator:
    def validate_product_create(self, product: schemas.ProductCreate):
        if product.price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")

    def validate_product_update(self, product: schemas.ProductUpdate):
        if product.price and product.price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")
