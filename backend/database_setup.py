from flask import Flask
from application import db
from application.models import *
from application.dal import *
import random


def setup_initial_data():
    roles = {1: 'admin', 2: 'seller', 3: 'buyer'}
    for role_id, role_name in roles.items():
        existing_role = db.session.query(
            Role).filter_by(role_id=role_id).first()
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
        product = ProductDAL.create(category_id=category.category_id, created_by=1,
                                    product_name=products[i]['product_name'], description=products[i]['description'])
    print("Categories and products initialized.")


def initialize_dummy_users():
    try:
        buyer1 = UserDAL.create(username='buyer1', email='buyer1@example.com',
                                password='buyer1password', contact="1234567890", address="10 buyer1 Street", roles=[3])

        buyer2 = UserDAL.create(username='buyer2', email='buyer2@example.com',
                                password='buyer2password', contact="1234509876", address="10 buyer2 Street", roles=[3])

        seller1 = UserDAL.create(username='seller1', email='seller1@example.com',
                                 password='seller1password', contact="9876543210", address="10 seller1 Street", roles=[2])

        seller2 = UserDAL.create(username='seller2', email='seller2@example.com',
                                 password='seller2password', contact="9876123450", address="10 seller2 Street", roles=[2])
        buyers = [buyer1, buyer2]
        sellers = [seller1, seller2]
        print("buyer and seller created successfully with IDs: ",
              buyer1.user_id, seller1.user_id, " respectively")
    except Exception as e:
        print("Could not create buyers and sellers due to: ", e.args[0])
    return (buyers, sellers)


def initialize_dummy_pending_bids(sellers: list[User]):
    products = ProductDAL.get_all_products()

    for i in range(3):
        product = random.choice(products)
        seller = random.choice(sellers)
        seller_id = seller.user_id
        ProductSellerDAL.create(product.product_id, seller_id, random.uniform(
            1, 100), random.randint(1, 100))
    print("Product bids created successfully")


def initialize_orders(buyers: list[User], sellers: list[User]):
    orders = []
    for j in range(2):
        items = []
        buyer = random.choice(buyers)
        buyer_id = buyer.user_id
        for i in range(3):
            seller = random.choice(sellers)
            while len(seller.product_bids) == 0:
                seller = random.choice(sellers)
            seller_id = seller.user_id
            product_bid = random.choice(seller.product_bids)
            product_bid = product_bid.to_json()
            quantity = random.randint(1, 10)
            item = {'seller_id': seller_id, 'product_id': product_bid['product']['product_id'],
                    'price': product_bid['price'], 'quantity': quantity}
            items.append(item)
        order = OrderDAL.create(buyer_id=buyer_id, items=items)
        orders.append(order)
    print("Order created successfully")
    return orders


def initialize_reviews(orders: list[Order]):
    reviews = []
    comments = [
        "A poor product. Doesn't work as it is supposed to. Don't buy",
        "A below average product. Can work but causes lot of hassle.", 
        "Average purchase. Better alternatives present in the market", 
        "Good product. Does what it's supposed and it's so easy to use.", 
        "What a fantastic product"
    ]
    for i in range(3):
        order = random.choice(orders)
        product = random.choice(order.orderitems)
        rating = random.choice([i * 0.5 for i in range(2, 11)])
        review = {
            'user_id': order.buyer_id,
            'product_id': product.product_id,
            'rating': rating,
            'comment':  comments[int(rating) - 1]
        }
        review = ReviewDAL.create(review['user_id'], review['product_id'], review['rating'], review['comment'])
        reviews.append(review)
        OrderDAL.mark_order_as_completed(product.orderitems_id)
    print("Reviews created successfully. ", [rev.to_json() for rev in reviews])
    return reviews

def initialize_database(app: Flask):
    with app.app_context():
        db.create_all()  # Create tables
        setup_initial_data()
        initialize_categories_and_products()
        buyers, sellers = initialize_dummy_users()
        initialize_dummy_pending_bids(sellers=sellers)
        orders = initialize_orders(buyers=buyers, sellers=sellers)
        reviews = initialize_reviews(orders=orders)