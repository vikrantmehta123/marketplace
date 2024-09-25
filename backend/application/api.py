from flask import Blueprint, request, jsonify
from .dal import *
from application.cache import cache

api = Blueprint('api', __name__, url_prefix='/api/v1')

# region User API

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    try:
        user = UserDAL.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            contact=data['contact'],
            address=data['address'],
            roles=data.get('roles', []) 
        )
        return jsonify(user.to_json()), 201
    except IntegrityError as ie:
        return jsonify({'error': 'User already exists'}), 404
    except Exception as e:
        return jsonify({'error': str(e.args[0])}), 404
    
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
        cache.delete('categories')
        return jsonify(category.to_json()), 201  # Created
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@api.route('/category', methods=['GET'])
@cache.cached(timeout=86400, key_prefix='categories') # Cache for 1 day
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
        cache.delete('categories')
        return jsonify(category.to_json()), 200  # OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@api.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = CategoryDAL.delete(category_id)
        cache.delete('categories')
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
    
    cache_key = f'products_by_category:{category_id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data), 200

    try:
        products = ProductDAL.get_products_by_category(category_id)
        products_list = [product.to_json() for product in products]

        cache.set(cache_key, products_list, timeout=86400)  # Cache products for one day

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

    cache_key = f'products_by_category:{category_id}'
    cache.delete(cache_key)

    try:
        product = ProductDAL.create(product_name, description, category_id, created_by)
        return jsonify(product.to_json()), 201  # Return the created product with a 201 status code
    except Exception as e:
        return jsonify({'message':str(e)}), 500


@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = ProductDAL.get_product_by_id(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404  # Return a 404 if not found

    # Update product with provided data
    try:
        updated_product = ProductDAL.update(product_id, **data)

        category_id = product.category_id
        cache_key = f'products_by_category:{category_id}'
        cache.delete(cache_key)

        cache_key = f'products_by_category:{updated_product.category_id}'
        cache.delete(cache_key)
        

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
        cache.delete_memoized(get_reviews_by_product, product_id)
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
@cache.memoize(timeout=86400)  # Cache for 1 day
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
        review = ReviewDAL.delete(review_id)

        product_id = review.product_id
        cache.delete_memoized(get_reviews_by_product, product_id)
        return jsonify({'message': 'Review deleted successfully'}), 204  # No Content
    except ValueError as e:
        return jsonify({'message': str(e)}), 404  # Not found
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
# endregion


# region ProductSellers
@api.route('/product-sellers', methods=['POST'])
def create_product_seller():
    """
    Create a new product seller.
    Expects JSON with product_id, seller_id, selling_price, and stock.
    """
    data = request.json
    product_id = data.get('product_id')
    seller_id = data.get('seller_id')
    selling_price = data.get('selling_price')
    stock = data.get('stock')

    try:
        product_seller = ProductSellerDAL.create(product_id, seller_id, selling_price, stock)
        return jsonify(product_seller.to_json()), 201  # Created
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
    
@api.route('/product-sellers/<int:productseller_id>', methods=['PUT'])
def update_product_seller(productseller_id):
    data = request.json
    selling_price = data.get('selling_price')
    stock = data.get('stock')

    try:
        updated_product_seller = ProductSellerDAL.update(productseller_id, selling_price, stock)
        return jsonify(updated_product_seller.to_json()), 200  # OK
    except ValueError as e:
        return jsonify({'message': str(e)}), 404  # Not found
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
    
@api.route('/product-sellers/<int:productseller_id>', methods=['GET', 'DELETE'])
def delete_product_seller(productseller_id):
    if request.method == "DELETE":
        try:
            ProductSellerDAL.delete(productseller_id)
            return jsonify({'message': 'Product seller deleted successfully'}), 204  # No Content
        except ValueError as e:
            return jsonify({'message': str(e)}), 404  # Not found
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # Bad request
    else:
        try:
            productseller = ProductSellerDAL.get_product_seller_by_id(productseller_id)
            return jsonify(productseller.to_json()), 200
        except ValueError as ve:
            return jsonify({'message':'Product Seller not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400  # Bad request
        
@api.route('/products/<int:product_id>/sellers', methods=['GET'])
def get_sellers_by_product(product_id):
    try:
        sellers = ProductSellerDAL.get_sellers_by_product(product_id)
        sellers_list = [seller.to_json() for seller in sellers]
        return jsonify(sellers_list), 200  # OK
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
# endregion

# region Order API
@api.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    buyer_id = data.get('buyer_id')
    items = data.get('items')

    try:
        order = OrderDAL.create(buyer_id=buyer_id, items=items)

        buyer_id = order.buyer_id
        cache_key = f"get_order_by_buyer:{buyer_id}"
        cache.delete(cache_key)

        cache.delete_memoized(get_order, order.order_id)

        return jsonify(order.to_json()), 201  # Created
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request

@api.route('/orders/<int:order_id>', methods=['GET'])
@cache.memoize(timeout=86400)
def get_order(order_id):
    order = OrderDAL.get_order_by_id(order_id)
    if order:
        return jsonify(order.to_json()), 200  # OK
    return jsonify({'message': 'Order not found'}), 404  # Not found

@api.route('/orders', methods=['GET'])
def get_order_by_buyer():
    data = request.json
    buyer_id = data.get('buyer_id')
    orderlist = OrderDAL.get_order_by_buyer(buyer_id=buyer_id)

    cache_key = f"get_order_by_buyer:{buyer_id}"
    cache.set(cache_key, orderlist, timeout=86400) 

    return jsonify(orderlist), 200

@api.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        deleted_order = OrderDAL.delete(order_id=order_id)

        buyer_id = deleted_order.buyer_id
        cache_key = f"get_order_by_buyer:{buyer_id}"
        cache.delete(cache_key)

        cache.delete_memoized(get_order, deleted_order.order_id)

        return jsonify(deleted_order.to_json()), 204  # No Content
    except ValueError as e:
        return jsonify({'message': str(e)}), 404  # Not found
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request
# endregion
