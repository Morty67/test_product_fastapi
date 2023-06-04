from datetime import datetime
from app.database.engine import Base
from sqlalchemy import Column, String, Integer, DateTime, Float


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<Product {self.name} - {self.description}>"
