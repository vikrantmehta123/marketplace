from flask import Flask
from application import db
from application.models import *
from application.dal import *
import random

def setup_initial_data():
    roles = {1: 'admin', 2: 'seller', 3: 'buyer'}
    for role_id, role_name in roles.items():
        existing_role = db.session.query(Role).filter_by(role_id=role_id).first()
        if existing_role is None:
            new_role = Role(role_id=role_id, role_name=role_name)
            db.session.add(new_role)
        else:
            print(f"Role '{role_name}' already exists.")

    db.session.commit()

    print("Roles Created: ", db.session.query(Role).all())

    admin = db.session.query(User).filter_by(username='admin').first()
    if admin is None:
        admin = UserDAL.create(username='admin', email='admin@example.com',
                               password='adminpassword', contact="1234567890", address="10 Dummy Street", roles=[1])

        print("Admin user created. ", admin)
    else:
        print("Admin user already exists.")


def initialize_categories_and_products():
    """Initialize categories in the database."""
    categories = [
        {
            "category_name": "Electronics",
        },
        {
            "category_name": "Home & Kitchen",
        },
        {
            "category_name": "Fashion",
        },
        {
            "category_name": "Health & Beauty",
        },
        {
            "category_name": "Sports & Outdoors",
        },
        {
            "category_name": "Books & Stationery",
        },
        {
            "category_name": "Toys & Games",
        }
    ]
    products = [
        {
            "product_name": "Smartphone X Pro",
            "description": "A high-performance smartphone with a stunning display, powerful processor, and exceptional camera capabilities."
        },
        {
            "product_name": "Stainless Steel Cookware Set",
            "description": "A 10-piece cookware set made of durable stainless steel, perfect for all your cooking needs."
        },
        {
            "product_name": "Men's Casual Jacket",
            "description": "A stylish and comfortable casual jacket that is perfect for everyday wear and can be paired with any outfit."
        },
        {
            "product_name": "Organic Skin Moisturizer",
            "description": "A lightweight moisturizer made from organic ingredients to keep your skin hydrated and radiant all day."
        },
        {
            "product_name": "Mountain Bike 26''",
            "description": "A rugged mountain bike designed for all terrains, featuring durable tires and a comfortable seat."
        },
        {
            "product_name": "The Great Gatsby - Hardcover",
            "description": "A beautifully bound edition of F. Scott Fitzgerald's classic novel, complete with a foreword and illustrations."
        },
        {
            "product_name": "Educational Building Blocks",
            "description": "A set of colorful building blocks that promotes creativity and learning through play for children aged 3 and up."
        }
    ]

    for i, cat in enumerate(categories):
        category = CategoryDAL.create(name=cat["category_name"]
        )
        product = ProductDAL.create(category_id=category.category_id, created_by=1, product_name=products[i]['product_name'], description=products[i]['description'])
    print("Categories and products initialized.")

def initialize_dummy_users():
    try:
        buyer = UserDAL.create(username='buyer', email='buyer@example.com',
                                password='buyerpassword', contact="1234567890", address="10 Buyer Street", roles=[3])
        seller = UserDAL.create(username='seller', email='seller@example.com',
                                password='sellerpassword', contact="1234567890", address="10 Seller Street", roles=[2])
        print("Buyer and seller created successfully with IDs: ", buyer.user_id, seller.user_id, " respectively")
    except Exception as e:
        print("Could not create buyers and sellers due to: ", e.args[0])
    return buyer, seller

def initialize_dummy_pending_bids(seller_id):
    products = ProductDAL.get_all_products()

    for i in range(3):
        product = random.choice(products)
        ProductSellerDAL.create(product.product_id, seller_id, random.uniform(1, 100), random.randint(1, 100))
    print("Product bids created successfully")

def initialize_database(app: Flask):
    with app.app_context():
        db.create_all()  # Create tables
        setup_initial_data()
        initialize_categories_and_products()
        buyer, seller = initialize_dummy_users()
        initialize_dummy_pending_bids(seller_id=seller.user_id)