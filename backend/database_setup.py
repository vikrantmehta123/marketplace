from flask import Flask
from application import db
from application.models import *
from application.dal import *


def setup_initial_data():
    roles = {1: 'admin', 2: 'editor', 3: 'viewer'}
    for role_id, role_name in roles.items():
        existing_role = db.session.query(
            Role).filter_by(role_id=role_id).first()
        if existing_role is None:
            new_role = Role(role_id=role_id, role_name=role_name)
            db.session.add(new_role)
        else:
            print(f"Role '{role_name}' already exists.")
    db.session.commit()
    admin = db.session.query(User).filter_by(username='admin').first()
    if admin is None:
        admin = UserDAL.create(username='admin', email='admin@example.com',
                               password='adminpassword', contact="1234567890", address="10 Dummy Street", roles=[1])

        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")


def initialize_categories():
    """Initialize categories in the database."""
    categories = [
        {
            "category_name": "Electronics",
            "category_description": "Explore the latest gadgets and devices, including smartphones, laptops, tablets, and accessories. Find top brands and cutting-edge technology to stay connected and entertained."
        },
        {
            "category_name": "Home & Kitchen",
            "category_description": "Discover a wide range of home and kitchen essentials, from cookware and appliances to furniture and décor. Transform your living space into a cozy and functional environment."
        },
        {
            "category_name": "Fashion",
            "category_description": "Shop the latest trends in clothing, shoes, and accessories for men, women, and children. Find stylish outfits for any occasion and express your personal style."
        },
        {
            "category_name": "Health & Beauty",
            "category_description": "Browse a variety of health and beauty products, including skincare, makeup, vitamins, and wellness items. Enhance your well-being and feel your best every day."
        },
        {
            "category_name": "Sports & Outdoors",
            "category_description": "Gear up for your favorite activities with our selection of sports equipment, outdoor gear, and apparel. Whether you're hiking, cycling, or working out, we have everything you need to stay active."
        },
        {
            "category_name": "Books & Stationery",
            "category_description": "Dive into a world of literature with our collection of books across various genres, from fiction and non-fiction to self-help and children's books. Find the perfect stationery for school or work."
        },
        {
            "category_name": "Toys & Games",
            "category_description": "Find fun and engaging toys and games for children of all ages. From educational toys to outdoor games, spark creativity and imagination with our curated selection."
        }
    ]
    products = [
        {
            "category_name": "Electronics",
            "product_name": "Smartphone X Pro",
            "description": "A high-performance smartphone with a stunning display, powerful processor, and exceptional camera capabilities."
        },
        {
            "category_name": "Home & Kitchen",
            "product_name": "Stainless Steel Cookware Set",
            "description": "A 10-piece cookware set made of durable stainless steel, perfect for all your cooking needs."
        },
        {
            "category_name": "Fashion",
            "product_name": "Men's Casual Jacket",
            "description": "A stylish and comfortable casual jacket that is perfect for everyday wear and can be paired with any outfit."
        },
        {
            "category_name": "Health & Beauty",
            "product_name": "Organic Skin Moisturizer",
            "description": "A lightweight moisturizer made from organic ingredients to keep your skin hydrated and radiant all day."
        },
        {
            "category_name": "Sports & Outdoors",
            "product_name": "Mountain Bike 26''",
            "description": "A rugged mountain bike designed for all terrains, featuring durable tires and a comfortable seat."
        },
        {
            "category_name": "Books & Stationery",
            "product_name": "The Great Gatsby - Hardcover",
            "description": "A beautifully bound edition of F. Scott Fitzgerald's classic novel, complete with a foreword and illustrations."
        },
        {
            "category_name": "Toys & Games",
            "product_name": "Educational Building Blocks",
            "description": "A set of colorful building blocks that promotes creativity and learning through play for children aged 3 and up."
        }
    ]

    for i, cat in enumerate(categories):
        category = CategoryDAL.create(name=cat["category_name"]
        )
        ProductDAL.create(category_id=category.category_id, created_by=1, product_name=products[i]['product_name'], description=products[i]['description'])
    print("Categories and products initialized.")


def initialize_database(app: Flask):
    with app.app_context():
        db.create_all()  # Create tables
        setup_initial_data()
        initialize_categories()