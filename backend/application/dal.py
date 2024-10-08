from sqlalchemy.exc import IntegrityError
from .models import *
import bcrypt
from .exceptions import *
from sqlalchemy import desc

SALT ="some-string"

# region CRUD operations for User
class UserDAL:
    @staticmethod
    def create(username:str, email:str, password:str, contact:str, address:str, roles:list[int]) -> User:
        if len(roles) == 0: 
            raise ValueError("Roles cannot be empty")
        for role in roles:
            if role not in [1, 2, 3]:
                raise ValueError("Roles cannot take invalid value")
            
        pw = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        user = User(username=username, email=email, password=pw, contact=contact, address=address)

        try:
            db.session.add(user)
            for role in roles:
                user_role = UserRole(user_id=user.user_id, role_id=role)
                db.session.add(user_role)
                user.roles.append(user_role)
            db.session.commit()      
        except IntegrityError as ie:
            db.session.rollback()
            raise ie  
        except Exception as e:
            db.session.rollback()
            raise e
        return user

    @staticmethod
    def get_user_by_id(user_id:int) -> User:
        user = db.session.get(User, user_id)
        return user
    
    @staticmethod
    def get_user_by_username(username:str) -> User:
        user = db.session.query(User).filter_by(username=username).first()
        return user

    @staticmethod
    def update(user_id:int, **kwargs) -> User:
        user = UserDAL.get_user_by_id(user_id=user_id)
        if not user: 
            raise ValueError("User not found")
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                db.session.rollback()
                raise AttributeError(f"User has no attribute '{key}'")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return user 
    
    @staticmethod
    def get_incomplete_sales_orders(user_id: int):
        try:
            incomplete_sales_orders = db.session.query(OrderItem).filter_by(seller_id=user_id, is_completed=False).all()
            
            return incomplete_sales_orders
        except Exception as e:
            raise e
# endregion

# region CRUD operations for Categories
class CategoryDAL:
    @staticmethod
    def create(name:str) -> Category:
        category = Category(category_name=name)
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return category

    @staticmethod
    def get_category_by_id(category_id:int) -> Category:
        category = db.session.get(Category, category_id)
        return category

    @staticmethod
    def update(category_id:int, category_name:str) -> Category:
        category = CategoryDAL.get_category_by_id(category_id=category_id)
        if not category: 
            raise ValueError("Category not found")
        try:
            category.category_name = category_name
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        return category
        
    @staticmethod
    def delete(category_id:int) -> Category:
        category = CategoryDAL.get_category_by_id(category_id=category_id)
        try:
            db.session.delete(category) # TODO: instead of deleting, create a flag for is_deleted
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return category
    
    @staticmethod 
    def get_all_categories() -> list[Category]:
        categories = db.session.query(Category).all()

        return categories
# endregion

# region CRUD operations for Reviews
class ReviewDAL:
    @staticmethod
    def create(user_id:int, product_id:int, rating:float, comment:str=None) -> Review:
        review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
        try:
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return review
    
    @staticmethod
    def get_review_by_id(review_id:int) -> Review:
        review = db.session.get(Review, review_id)
        return review

    @staticmethod
    def update(review_id:int, **kwargs) -> Review:
        review = ReviewDAL.get_review_by_id(review_id)
        if not review: 
            raise ValueError("Review not found")
        for key, value in kwargs.items():
            if hasattr(review, key):
                setattr(review, key, value)
            else:
                db.session.rollback()
                raise AttributeError(f"Review has no attribute '{key}'")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return review 

    @staticmethod
    def delete(review_id:int) -> Review:
        review = ReviewDAL.get_review_by_id(review_id)
        if not review:
            raise ValueError("Review not found")
        try:
            db.session.delete(review)
            db.session.commit()
        except Exception as e:
            raise e
        return review
    
    @staticmethod
    def get_reviews_by_product(product_id:int) -> list[Review]:
        reviews = db.session.query(Review).filter_by(product_id=product_id).all()
        return reviews

    @staticmethod
    def increment_upvote(review_id:int):
        review = ReviewDAL.get_review_by_id(review_id)
        review.upvotes += 1
        db.session.commit()
    
    @staticmethod
    def increment_downvotes(review_id:int):
        review = ReviewDAL.get_review_by_id(review_id)
        review.downvotes += 1
        db.session.commit()

    @staticmethod
    def fetch_top_reviews(product_id, limit=100):
        reviews = (
            db.session.query(Review)
            .filter_by(product_id = product_id)
            .order_by((Review.upvotes - Review.downvotes).desc())  # Order by score
            .limit(limit)
            .all()
        )
        return reviews
# endregion

class ProductDAL:
    @staticmethod
    def create(product_name:str, description:str, category_id:int, created_by:int) -> Product:
        product = Product(product_name=product_name, description=description, category_id=category_id, created_by=created_by)
        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return product

    @staticmethod
    def get_product_by_id(product_id:int) -> Order:
        product = db.session.get(Product, product_id)
        return product

    @staticmethod
    def update(product_id:int, **kwargs) -> Order:
        product = ProductDAL.get_product_by_id(product_id=product_id)
        if not product: 
            raise ValueError("Product not found")
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
            else:
                db.session.rollback()
                raise AttributeError(f"Product has no attribute '{key}'")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return product 
    
    @staticmethod
    def get_products_by_category(category_id:int) -> list[Product]:
        category = CategoryDAL.get_category_by_id(category_id=category_id)
        return category.products
    
    @staticmethod
    def get_all_products() -> list[Product]:
        products = db.session.query(Product).all()
        return products

class ProductSellerDAL:
    @staticmethod
    def create(product_id: int, seller_id: int, selling_price: float, stock: int) -> ProductSellers:
        new_product_seller = ProductSellers(
            product_id=product_id,
            seller_id=seller_id,
            selling_price=selling_price,
            stock=stock
        )
        try:
            db.session.add(new_product_seller)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return new_product_seller
    
    @staticmethod
    def update(productseller_id: int, selling_price: float = None, stock: int = None) -> ProductSellers:
        
        product_seller = db.session.query(ProductSellers).filter_by(productseller_id=productseller_id).first()
        if not product_seller:
            raise ValueError(f"No ProductSeller found with ID {productseller_id}")
        
        try:
            if selling_price is not None:
                product_seller.selling_price = selling_price
            if stock is not None:
                product_seller.stock = stock
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return product_seller
    @staticmethod
    def delete(productseller_id: int) -> None:

        product_seller = db.session.query(ProductSellers).filter_by(productseller_id=productseller_id).first()
        if not product_seller:
            raise ValueError(f"No ProductSeller found with ID {productseller_id}")
        try:
            db.session.delete(product_seller)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return product_seller
    
    @staticmethod
    def get_sellers_by_product(product_id: int):
        results = db.session.query(ProductSellers).filter_by(product_id=product_id).order_by(desc(ProductSellers.selling_price)).all()
        output = [ ]
        for res in results:
            res_json = { 
                'productseller_id': res.productseller_id,
                'stock' : res.stock, 
                'price' : res.selling_price, 
                'seller': {
                    'username': res.seller.username, 
                    'contact':res.seller.contact
                }
            }
            output.append(res_json)
        
        return output

    @staticmethod
    def get_products_by_seller(seller_id: int) -> list[ProductSellers]:
        seller = UserDAL.get_user_by_id(seller_id)
        res = { 'seller' : str(seller) }
        res['product_bids'] = [ ]
        for bid in seller.product_bids:
            res["product_bids"].append(bid.to_json())
        return res
    
    @staticmethod
    def get_product_seller_by_id(id:int) -> ProductSellers:
        productseller = db.session.get(ProductSellers, id)
        if not productseller:
            raise ValueError("Productseller not found")
        return productseller
    
class OrderDAL:
    @staticmethod
    def create(buyer_id:int, items:list[dict]) -> Order:
        order = Order(buyer_id=buyer_id)
        db.session.add(order)
        
        try:
            for item in items:
                order_item = OrderItem(
                    seller_id=item['seller_id'],
                    product_id=item['product_id'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                order.orderitems.append(order_item)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e 
        return order

    @staticmethod
    def get_order_by_id(order_id:int) -> Order:
        order = db.session.get(Order, order_id)
        return order
    
    @staticmethod
    def get_order_by_buyer(buyer_id:int) -> list[Order]:
        return db.session.query(Order).filter_by(buyer_id=buyer_id).all()

    @staticmethod
    def update(order_id:int,  items: list[dict] = None) -> Order:
        order = OrderDAL.get_order_by_id(order_id=order_id)
        if not order:
            raise ValueError("Order not found")
        # TODO: update logic for orderitems


    @staticmethod
    def delete(order_id:int) -> Order:
        order = OrderDAL.get_order_by_id(order_id=order_id)
        # if order is None:
        #     raise ValueError("Order doesn't exist")
        
        for item in order.orderitems:
            if item.is_completed:
                CancellationNotPossibleError("Order has already been dispatched")

        try:
            db.session.delete(order) 
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return order
    
    @staticmethod
    def mark_order_as_completed(orderitem_id:int):
        orderitem = db.session.get(OrderItem, orderitem_id)
        orderitem.is_completed = True
        db.session.commit()
    

class WishlistDAL:
    @staticmethod 
    def create(user_id:int, wishlist_name:str)->Wishlist:
        """Creates an empty wishlist with the given name for the user"""
        pass

    @staticmethod
    def update(wishlist_id:int, wishlist_name:str) -> Wishlist:
        """Lets users change name of their wishlist"""
        pass

    @staticmethod 
    def delete(wishlist_id:int):
        """Lets users delete their wishlist and associated items"""

    @staticmethod
    def add_item_to_wishlist(wishlist_id:int, product_id:int):
        """lets users add products to their wishlist"""

    @staticmethod
    def delete_item_from_wishlist(wishlist_id:int, product_id:int):
        """Lets users delete product from their wishlist"""
