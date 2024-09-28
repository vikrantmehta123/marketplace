from .models import *
"""
This module defines Serializer methods for every model
"""


def serialize_user(user: User) -> dict:
    return {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'contact': user.contact,
        'address': user.address,
        'roles': [serialize_role(role) for role in user.roles]
    }


def serialize_role(role: Role) -> dict:
    return {
        "role_id": role.role_id,
        'role_name': role.role_name
    }


def serialize_category(category: Category) -> dict:
    return {
        'category_id': category.category_id,
        'category_name': category.category_name
    }

def serialize_product(product:Product) -> dict:
    """Convert the Product instance to a JSON-compatible dict."""
    return {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'description': product.description,
        'category': {
            'category_id': product.category.category_id,
            'category_name': product.category.category_name
        }
    }

def serialize_product_bids(product_bid:ProductSellers) -> dict:
    """Convert the ProductSellers instance to a JSON-compatible dict."""
    return {
        'productseller_id': product_bid.productseller_id,
        # Ensure product is a dict
        'product': serialize_product(product_bid.product),
        'stock': product_bid.stock,
        'price': product_bid.selling_price,
    }

def serialize_review(review:Review) -> dict:
    return {
        'review_id': review.review_id, 
        'user_id' : review.user_id, 
        'product_id' : review.product_id, 
        'rating' : review.rating, 
        'comment':review.comment
    }
