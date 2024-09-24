from flask import Blueprint, request, jsonify
from .dal import *

api = Blueprint('api', __name__, url_prefix='/api/v1')

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
    category_id = request.args.get('category_id')
    
    if not category_id:
        return jsonify({"error": "category_id is required"}), 400 
    
    try:
        products = ProductDAL.get_products_by_category(category_id)
        products_list = [product.to_json() for product in products]

        return jsonify(products_list), 200 
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@api.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductDAL.get_product_by_id(product_id)
    if product:
        return jsonify(product.to_json())
    return jsonify({'message': 'Product not found'}), 404  # Return a 404 if not found

@api.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product_name = data.get('product_name')
    description = data.get('description')
    category_id = data.get('category_id')
    created_by = data.get('created_by')

    product = ProductDAL.create(product_name, description, category_id, created_by)
    return jsonify(product.to_json()), 201  # Return the created product with a 201 status code

@api.route('/api/products/<int:product_id>', methods=['PUT'])
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