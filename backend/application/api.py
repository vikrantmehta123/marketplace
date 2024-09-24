from flask import Blueprint, request, jsonify
from .dal import *

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/')
def hello():
    return "hello"

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
        print(e.args[0])
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
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

# endregion