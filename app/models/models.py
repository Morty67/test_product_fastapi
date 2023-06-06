from datetime import datetime

from sqlalchemy.orm import relationship

from app.database.engine import Base
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} - {self.description}>"


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
