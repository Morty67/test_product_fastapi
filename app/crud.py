from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import Product, Category
from app.serializers.schemas import ProductCreate


async def get_all_products(db: AsyncSession, offset: int, limit: int):
    stmt = select(Product).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_products_sorted_by_price(
    db: AsyncSession, offset: int, limit: int
):
    stmt = select(Product).order_by(Product.price).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalar()


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(
    db: AsyncSession, product_id: int, product: ProductCreate
):
    db_product = await db.get(Product, product_id)
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    category = await db.get(Category, product.category_id)
    db_product.category = category
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await db.get(Product, product_id)
    db.delete(db_product)
    await db.commit()
    return db_product
