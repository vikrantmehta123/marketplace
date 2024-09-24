from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import datetime
from flask_sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class TimestampMixin:
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False,)

@dataclass
class User(TimestampMixin, db.Model):
    user_id: int
    email: str
    username: str
    password: str
    contact: str
    address: str

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(125), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    contact = Column(String(10), nullable=False)
    address = Column(String(255), nullable=False)

class Role(db.Model):
    role_id: int
    role_name:str

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(120), unique=True, nullable=False)

@dataclass
class UserRole(db.Model):
    userrole_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    role_id = Column(Integer, ForeignKey('role.role_id'))

    user = relationship('User', backref='roles')

@dataclass
class Category(db.Model):
    category_id : int
    category_name: str

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(120), unique=True, nullable=False)

@dataclass
class Product(TimestampMixin, db.Model):
    product_id:int
    product_name:str
    description:str

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('user.user_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))

    category = relationship('Category', backref='products')

@dataclass
class ProductSellers(TimestampMixin, db.Model):
    productseller_id:int
    product_id:int
    seller_id:int
    selling_price:float
    stock:int

    product_id = Column(Integer, ForeignKey('product.product_id'))
    seller_id = Column(Integer, ForeignKey('user.user_id'))
    selling_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)    

    seller = relationship('User', backref="products")
    product = relationship('Product', backref='sellers')

@dataclass
class Review(TimestampMixin, db.Model):
    review_id: int
    user_id: int
    product_id:int
    rating: float
    comment:str

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)

    user = relationship('User', backref='reviews')
    product = relationship('Product', backref='reviews')

@dataclass
class Order(TimestampMixin, db.Model):
    order_id:int
    buyer_id:int

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', backref='purchase_orders')

@dataclass
class OrderItems(db.Model):
    order_id:int
    seller_id:int
    product_id:int
    price:float
    quantity:int
    is_completed:bool

    order_id = Column(Integer, ForeignKey('Order.order_id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)

    seller = relationship('User', backref='sales_orders')
    order = relationship('Order', backref='orderdetails')
    product = relationship('Product', backref='orders')