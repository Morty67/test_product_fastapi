from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.product_service import ProductService, ProductValidator
from app.database.engine import SessionLocal
from app.serializers import schemas

app = FastAPI(
    title="Product Management",
)

product_service = ProductService()
product_validator = ProductValidator()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/", response_model=list[schemas.Product])
def read_all_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db=db)


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    product_validator.validate_product_create(product)
    db_product = product_service.create_product(db=db, product=product)
    return db_product


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    product_validator.validate_product_update(product)
    db_product = product_service.update_product(
        db=db, product_id=product_id, product=product
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not product_service.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
