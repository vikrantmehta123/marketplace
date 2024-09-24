from flask import Blueprint, request, jsonify
from .dal import *

api = Blueprint('api', __name__, url_prefix='/api/v1')

# region User API

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    user = UserDAL.create(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        contact=data['contact'],
        address=data['address'],
        roles=data.get('roles', []) 
    )
    return jsonify(user.to_json()), 201


@api.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserDAL.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_json()), 200
    return jsonify({'error': 'User not found'}), 404

@api.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    user = UserDAL.get_user_by_username(username=username)
    if user:
        return jsonify(user.to_json()), 200
    return jsonify({'error': 'User not found'}), 404


@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    try:
        user = UserDAL.update(user_id, **data)
        return jsonify(user.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except AttributeError as e:
        return jsonify({'error': str(e)}), 400
# endregion

# region API for Category
@api.route('/category', methods=['POST'])
def create_category():
    data = request.json 
    category_name = data.get('name')
    
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400
    
    try:
        category = CategoryDAL.create(name=category_name)
        return jsonify(category.to_json()), 201  # Created
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@api.route('/category', methods=['GET'])
def get_all_categories():
    categories = CategoryDAL.get_all_categories()
    categories = [category.to_json() for category in categories]
    return jsonify(categories), 200

@api.route('/category/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:
        category = CategoryDAL.get_category_by_id(category_id)
        if category:
            return jsonify(category.to_json()), 200  # OK
        else:
            return jsonify({"error": "Category not found"}), 404  # Not Found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@api.route('/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json  # Expecting JSON input
    category_name = data.get('name')
    
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400  # Bad Request
    
    try:
        category = CategoryDAL.update(category_id=category_id, category_name=category_name)
        return jsonify(category.to_json()), 200  # OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@api.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = CategoryDAL.delete(category_id)
        return jsonify({"message": "Category deleted successfully", "category": category.to_json()}), 200  # OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

# endregion

# region API for Products

@api.route('/products', methods=['GET'])
def get_products_by_category():
    data = request.json
    category_id = data.get('category_id')
    
    if not category_id:
        return jsonify({"error": "category_id is required"}), 400 
    
    try:
        products = ProductDAL.get_products_by_category(category_id)
        products_list = [product.to_json() for product in products]

        return jsonify(products_list), 200 
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductDAL.get_product_by_id(product_id)
    if product:
        return jsonify(product.to_json())
    return jsonify({'message': 'Product not found'}), 404  # Return a 404 if not found

@api.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product_name = data.get('product_name')
    description = data.get('description')
    category_id = data.get('category_id')
    created_by = data.get('created_by')

    product = ProductDAL.create(product_name, description, category_id, created_by)
    return jsonify(product.to_json()), 201  # Return the created product with a 201 status code

@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = ProductDAL.get_product_by_id(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404  # Return a 404 if not found

    # Update product with provided data
    try:
        updated_product = ProductDAL.update(product_id, **data)
        return jsonify(updated_product.to_json())
    except AttributeError as e:
        return jsonify({'message': str(e)}), 400  # Return a 400 for bad requests


# endregion

# region Review API
@api.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment', None)

    try:
        review = ReviewDAL.create(user_id, product_id, rating, comment)
        return jsonify(review.to_json()), 201  # Created
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request

@api.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = ReviewDAL.get_review_by_id(review_id)
    if review:
        return jsonify(review.to_json()), 200  # OK
    return jsonify({'message': 'Review not found'}), 404  # Not found

@api.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews_by_product(product_id):
    try:
        reviews = ReviewDAL.get_reviews_by_product(product_id)
        reviews_list = [review.to_json() for review in reviews]
        return jsonify(reviews_list), 200  # OK
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@api.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.json
    print(data)
    try:
        updated_review = ReviewDAL.update(review_id, **data)
        return jsonify(updated_review.to_json()), 200  # OK
    except ValueError as e:
        return jsonify({'message': str(e)}), 404  # Not found
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request

@api.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        ReviewDAL.delete(review_id)
        return jsonify({'message': 'Review deleted successfully'}), 204  # No Content
    except ValueError as e:
        return jsonify({'message': str(e)}), 404  # Not found
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
# endregion