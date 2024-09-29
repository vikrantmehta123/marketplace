from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from dataclasses import dataclass, field
import dataclasses
import datetime
from flask_sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.sql import func
import json


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __init__(self) -> None:
        self.created_at = func.now()
        self.updated_at = func.now()


class Base(MappedAsDataclass, DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Role(db.Model):
    """
    { 
        1: Admin, 
        2: Seller, 
        3: Buyer
    }
    """

    role_id = mapped_column(Integer, init=False, primary_key=True)
    role_name: Mapped[str] = mapped_column(
        unique=True, nullable=False, init=False)

    def __init__(self, role_id, role_name) -> None:
        super().__init__()
        self.role_id = role_id
        self.role_name = role_name

    def __repr__(self) -> str:
        res = {'role_id': self.role_id, 'role_name': self.role_name}
        return json.dumps(res)


class User(db.Model):
    user_id = mapped_column(Integer, primary_key=True,
                            autoincrement=True, nullable=False)
    username: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False, init=False)
    contact: Mapped[str] = mapped_column(nullable=False, init=False)
    address: Mapped[str] = mapped_column(nullable=False, init=False)

    product_bids: Mapped[list['ProductSellers']] = relationship(
        'ProductSellers', back_populates='seller')

    def __init__(self, username: str, email: str, password: str, contact: str, address: str) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.contact = contact
        self.address = address

    def to_json(self) -> dict:
        """Convert the User instance to a JSON-compatible dict."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'contact': self.contact,
            'address': self.address
        }

    def __str__(self) -> str:
        """Return a JSON string representation of the object."""
        return json.dumps(self.to_json())


class UserRole(db.Model):
    userrole_id = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.user_id'), init=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('role.role_id'), init=False)

    user = relationship('User', backref='roles', repr=False)
    role = relationship('Role', backref='users')

    def __init__(self, user_id, role_id) -> None:
        super().__init__()
        self.user_id = user_id
        self.role_id = role_id


class Category(db.Model):
    category_id = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=True)
    category_name: Mapped[str] = mapped_column(
        unique=True, nullable=False, init=False)

    products = relationship('Product', back_populates='category')

    def __init__(self, category_name) -> None:
        super().__init__()
        self.category_name = category_name

    def to_json(self) -> dict:
        return {
            'category_id': self.category_id,
            'category_name': self.category_name
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_json())


class Product(db.Model):
    product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.user_id'))
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('category.category_id', ondelete='CASCADE'))

    category: Mapped['Category'] = relationship(
        'Category', back_populates='products')
    sellers: Mapped[list['Product']] = relationship(
        'ProductSellers', back_populates='product')

    def __init__(self, product_name: str, description: str, created_by: int, category_id: int) -> None:
        super().__init__()
        self.product_name = product_name
        self.description = description
        self.created_by = created_by
        self.category_id = category_id

    def to_json(self) -> dict:
        """Convert the Product instance to a JSON-compatible dict."""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'description': self.description,
            'category': {
                'category_id': self.category.category_id,
                'category_name': self.category.category_name
            }
        }

    def __repr__(self) -> str:
        """Return a JSON string representation of the object."""
        return json.dumps(self.to_json())


class ProductSellers(db.Model):
    productseller_id = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    product_id = mapped_column(Integer, ForeignKey(
        'product.product_id'), init=False)
    seller_id = mapped_column(Integer, ForeignKey('user.user_id'), init=False)
    selling_price = mapped_column(Float, nullable=False)
    stock = mapped_column(Integer, nullable=False)

    seller = relationship('User', back_populates="product_bids")
    product = relationship('Product', back_populates='sellers')

    def __init__(self, product_id: int, seller_id: int, selling_price: float, stock: int) -> None:
        super().__init__()
        self.product_id = product_id
        self.seller_id = seller_id
        self.selling_price = selling_price
        self.stock = stock

    def to_json(self):
        """Convert the ProductSellers instance to a JSON-compatible dict."""
        return {
            'productseller_id': self.productseller_id,
            # Ensure product is a dict
            'product': json.loads(str(self.product)),
            'stock': self.stock,
            'price': self.selling_price,
        }

    def __repr__(self) -> str:
        """Return a JSON string representation of the object."""
        return json.dumps(self.to_json(), default=str)


class Review(db.Model):
    review_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('user.user_id'))
    product_id = mapped_column(Integer, ForeignKey('product.product_id'))
    rating = mapped_column(Float, nullable=False)
    comment = mapped_column(Text, nullable=True)

    user = relationship('User', backref='reviews', repr=False)
    product = relationship('Product', backref='reviews', repr=False)

    def __init__(self, user_id: int, product_id: int, rating: float, comment: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment

    def to_json(self) -> dict:
        return {
            'review_id' : self.review_id, 
            'product_id' : self.product_id, 
            'rating' : self.rating, 
            'comment' : self.comment, 
            'user': {
                'username' : self.user.username
            }
        }


class Order(db.Model):
    __tablename__ = 'order'  # Specify the table name

    order_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    buyer_id = mapped_column(Integer, ForeignKey(
        'user.user_id'), nullable=False)

    buyer = relationship('User', backref='purchase_orders', repr=False)
    orderitems: Mapped[list['OrderItem']] = relationship(
        'OrderItem', back_populates='order', cascade='all, delete')

    def __init__(self, buyer_id: int) -> None:
        super().__init__()
        self.buyer_id = buyer_id

    def to_json(self):
        return {
            'order_id': self.order_id,
            'buyer': {
                'user_id': self.buyer.user_id,
                'username': self.buyer.username, 
                'address': self.buyer.address, 
                'contact':self.buyer.contact
            }
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    orderitems_id = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    order_id = mapped_column(Integer, ForeignKey(
        'order.order_id'), nullable=False)
    seller_id = mapped_column(
        Integer, ForeignKey('user.user_id'), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(
        'product.product_id'), nullable=False)
    price = mapped_column(Float, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    is_completed = mapped_column(Boolean, default=False)

    seller: Mapped['User'] = relationship('User', backref='sales_orders',
                                          lazy='select', repr=False)
    product: Mapped['Product'] = relationship(
        'Product', backref='orders', repr=False)
    order: Mapped[Order] = relationship(
        'Order', back_populates='orderitems')

    def __init__(self, seller_id: int, product_id: int, price: float, quantity: int, is_completed=False) -> None:
        super().__init__()
        self.seller_id = seller_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.is_completed = is_completed

    def to_json(self):
        return {
            'order_id': self.order_id,
            'product': {
                'product_id': self.product.product_id,
                'product_name': self.product.product_name
            },
            'is_completed': self.is_completed,
            'price': self.price,
            'quantity': self.quantity,
            'seller': {
                'seller_id': self.seller.user_id,
                'username': self.seller.username
            }, 
            'order': self.order.to_json()
        }


class Wishlist(db.Model):
    wishlist_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey(
        'user.user_id'), nullable=False)
    wishlist_name = mapped_column(String(255), nullable=False)

    user = relationship('User', backref='wishlist')
    wishlist_items = relationship(
        'WishlistItems', backref='wishlist', cascade='all, delete', repr=False)


class WishlistItems(db.Model):
    wishlist_itemid = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    product_id = mapped_column(Integer, ForeignKey(
        'product.product_id'), nullable=False)
    wishlist_id = mapped_column(Integer, ForeignKey(
        'wishlist.wishlist_id'), nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey(
        'user.user_id'), nullable=False)

    # Relationship to CartItems
    cartitems = relationship("CartItems", backref='cart',
                             cascade='all, delete', repr=False)


class CartItems(db.Model):

    __tablename__ = 'cartitems'

    cartitems_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id = mapped_column(Integer, ForeignKey(
        'cart.cart_id'), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(
        'product.product_id'), nullable=False)
    quantity = mapped_column(Integer, nullable=False)
