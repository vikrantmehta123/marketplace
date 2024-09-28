from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from dataclasses import dataclass, field
import dataclasses
import datetime
from flask_sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

@dataclass
class TimestampMixin:
    created_at:datetime.datetime
    updated_at:datetime.datetime

    created_at = Column(TIMESTAMP, default=datetime.datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False,)

@dataclass
class Role(db.Model):
    """
    { 
        1: Admin, 
        2: Seller, 
        3: Buyer
    }
    """

    role_id: int = field(init=False, default=None)
    role_name:str

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(120), unique=True, nullable=False)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class User(db.Model, TimestampMixin):
    user_id: int = field(init=False, default=None)
    username: str
    email: str
    contact: str
    address: str
    roles: list['Role'] = field(default_factory=list)

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(125), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    contact = Column(String(10), nullable=False)
    address = Column(String(255), nullable=False)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class UserRole(db.Model):
    userrole_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    role_id = Column(Integer, ForeignKey('role.role_id'))

    user = relationship('User', backref='roles')
    role = relationship('Role', backref='users') 


    def to_json(self) -> dict:
        return dataclasses.asdict(self)
@dataclass
class Category(db.Model):
    category_id : int
    category_name: str
    products:list['Product'] = field(default_factory=list)

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(120), unique=True, nullable=False)

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class Product( db.Model, TimestampMixin):
    product_id:int = field(init=False, default=None)
    product_name:str
    description:str
    category_id:int
    reviews:list['Review'] = field(default_factory=list)
    sellers:list['User'] = field(default_factory=list)
    orders:list['OrderItems'] = field(default_factory=list)

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('user.user_id'))
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete='CASCADE'))

    category = relationship('Category', backref='products')

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class ProductSellers(db.Model, TimestampMixin):
    productseller_id:int
    product_id:int
    seller_id:int
    selling_price:float
    stock:int

    productseller_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    seller_id = Column(Integer, ForeignKey('user.user_id'))
    selling_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)    

    seller = relationship('User', backref="product_bids")
    product = relationship('Product', backref='sellers')
    
    def to_json(self) -> dict:
        return dataclasses.asdict(self)
    
@dataclass
class Review(db.Model, TimestampMixin):
    review_id: int = field(init=False, default=None)
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

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class Order(db.Model, TimestampMixin):
    order_id:int
    buyer_id:int
    orderitems: list['OrderItems'] = field(default_factory=list)

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    buyer = relationship('User', backref='purchase_orders')
    orderitems = relationship('OrderItems', backref='order', cascade='all, delete')

    def to_json(self) -> dict:
        return dataclasses.asdict(self)

@dataclass
class OrderItems(db.Model):
    orderitems_id:int
    order_id:int
    seller_id:int
    product_id:int
    price:float
    quantity:int
    is_completed:bool

    orderitems_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)

    seller = relationship('User', backref='sales_orders')
    product = relationship('Product', backref='orders')

    def to_json(self) -> dict:
        return dataclasses.asdict(self)
    

@dataclass
class Wishlist(db.Model):
    wishlist_id:int
    user_id:int
    wishlist_name:str

    wishlist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    wishlist_name = Column(String(255), nullable=False)

    user = relationship('User', backref='wishlist')
    wishlist_items = relationship('WishlistItems', backref='wishlist', cascade='all, delete')

@dataclass
class WishlistItems(db.Model, TimestampMixin):
    wishlist_id:int
    wishlist_itemid : int
    product_id: int

    wishlist_itemid = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    wishlist_id = Column(Integer, ForeignKey('wishlist.wishlist_id'), nullable=False)

