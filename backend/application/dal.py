from sqlalchemy.exc import IntegrityError
from models import *

class UserDAL:
    @staticmethod
    def create() -> User:
        pass

    @staticmethod
    def read_user_by_id(user_id:int) -> User:
        user = User.query.get(user_id)
        return user
    
    @staticmethod
    def read_user_by_username(username:str) -> User:
        user = User.query.filter_by(username= username).first()
        return user

    @staticmethod
    def update() -> User:
        pass

    @staticmethod
    def delete() -> User:
        pass

# region CRUD operations for Categories
class CategoryDAL:
    @staticmethod
    def create(name:str) -> Category:
        category = Category(name=name)
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return category

    @staticmethod
    def read_category_by_id(category_id:int) -> Category:
        category = Category.query.get(category_id)
        return category

    @staticmethod
    def update(category_id:int, category_name:str):
        category = Category.query.get(category_id)
        if category:
            category.category_name = category_name
            db.session.commit()
            return category
        else:
            raise ValueError("Category not found")
        
    @staticmethod
    def delete(category_id:int) -> Category:
        category = Category.query.get(category_id)
        try:
            db.session.delete(category) # TODO: instead of deleting, create a flag for is_deleted
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return category

# endregion

# region CRUD operations for Reviews
class ReviewDAL:
    def create(user_id:int, product_id:int, rating:float, comment:str=None) -> Review:
        review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
        try:
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return review
    
    def update(review_id:int) -> Review:
        pass

    def delete(review_id:int) -> Review:
        pass
# endregion

class ProductDAL:
    @staticmethod
    def create() -> Product:
        pass

    @staticmethod
    def get_product_by_id() -> Order:
        pass

    @staticmethod
    def update() -> Order:
        pass
    
    @staticmethod
    def delete() -> Order:
        pass

class OrderDAL:
    @staticmethod
    def create() -> Order:
        pass

    @staticmethod
    def get_order_by_id(order_id:int) -> Order:
        order = Order.query.get(order_id)
        return order

    @staticmethod
    def update() -> Order:
        pass

    @staticmethod
    def delete(order_id:int) -> Order:
        order = OrderDAL.get_order_by_id(order_id=order_id)
        if order:
            db.session.delete(order) # TODO: Before deleting, you need to check if any of the orderdetails are dispatched
            db.session.commit()
            return order
        else:
            db.session.rollback()
            raise ValueError("Order doesn't exist")
        