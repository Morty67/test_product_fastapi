from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Category
from app.services.product_service import ProductService, ProductValidator
from app.database.engine import async_session
from app.serializers import schemas

app = FastAPI(
    title="Product Management",
)

product_service = ProductService()
product_validator = ProductValidator()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.get("/products/", response_model=List[schemas.Product])
async def read_all_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    products = await product_service.get_all_products(
        db=db, offset=offset, limit=per_page
    )
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product_by_id(
        db=db, product_id=product_id
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    product_validator.validate_product_create(product)
    db_product = await product_service.create_product(db=db, product=product)
    return db_product


@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    product_validator.validate_product_update(product)
    db_product = await product_service.update_product(
        db=db, product_id=product_id, product=product
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    if not await product_service.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


@app.get("/categories/", response_model=List[schemas.Category])
async def get_all_categories(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return categories


@app.post("/categories", response_model=schemas.Category)
async def create_category(
    category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)
):
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@app.get("/categories/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Category).filter(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalar()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/categories/{category_id}", response_model=schemas.Category)
async def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Category).filter(Category.id == category_id)
    result = await db.execute(stmt)
    db_category = result.scalar()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    await db.commit()
    await db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}")
async def delete_category(
    category_id: int, db: AsyncSession = Depends(get_db)
):
    stmt = select(Category).filter(Category.id == category_id)
    result = await db.execute(stmt)
    db_category = result.scalar()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(db_category)
    await db.commit()
    return {"message": "Category deleted successfully"}
