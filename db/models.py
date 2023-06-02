from datetime import datetime
from db.engine import Base
from sqlalchemy import Column, String, Integer,  DateTime


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<Product {self.name} - {self.description}>"
