from sqlalchemy.orm import Session

from app.models.models import Product, Category
from app.serializers.schemas import ProductCreate


def get_all_products(db: Session, offset: int, limit: int):
    return db.query(Product).offset(offset).limit(limit).all()


def get_all_products_sorted_by_price(db: Session, offset: int, limit: int):
    return (
        db.query(Product)
        .order_by(Product.price)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    category = db.query(Category).get(product.category_id)
    db_product.category = category
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product
