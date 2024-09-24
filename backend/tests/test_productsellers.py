import pytest

BASE_URL = "http://127.0.0.1:5000/api/v1"

@pytest.fixture
def init_data(client):
    client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    client.post(f'{BASE_URL}/category', json={'name': 'Home Appliances'})
    user_response = client.post(f'{BASE_URL}/users', json={
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'securepassword',
        'contact': '1234567890',
        'address': '123 Main St',
        'roles': [1, 2, 3]  # Example roles
    })
    user = user_response.get_json()

    datalist = [
        {
            'product_name': 'Product1',
            'description': 'Product Description1',
            'category_id': 1,
            'created_by': 1
        },
        {
            'product_name': 'Product2',
            'description': 'New Product Description',
            'category_id': 2,
            'created_by': 1
        },
        {
            'product_name': 'Product3',
            'description': 'Product Description3',
            'category_id': 1,
            'created_by': 1
        }
    ]

    data_responses = []
    for data in datalist:
        response = client.post(f'{BASE_URL}/products', json=data)
        data_responses.append(response.get_json())
    return user, data_responses


def test_create_product_seller(client, init_data):
    user, productlist = init_data
    product = productlist[0]
    response = client.post(f'{BASE_URL}/product-sellers', json={
        'product_id': product['product_id'],
        'seller_id': user['user_id'],
        'selling_price': 19.99,
        'stock': 100
    })

    assert response.status_code == 201
    assert 'productseller_id' in response.json


def test_update_product_seller(client, init_data):
    user, productlist = init_data
    product = productlist[0]
    # First, create a product seller
    response = client.post(f'{BASE_URL}/product-sellers', json={
        'product_id': product['product_id'],
        'seller_id': user['user_id'],
        'selling_price': 19.99,
        'stock': 100
    })
    productseller_id = response.json['productseller_id']

    # Now, update the created product seller
    response = client.put(f'{BASE_URL}/product-sellers/{productseller_id}', json={
        'selling_price': 24.99,
        'stock': 80
    })
    assert response.status_code == 200
    assert response.json['selling_price'] == 24.99
    assert response.json['stock'] == 80

def test_delete_product_seller(client, init_data):
    user, productlist = init_data
    product = productlist[0]
    # Create a product seller
    response = client.post(f'{BASE_URL}/product-sellers', json={
        'product_id': product['product_id'],
        'seller_id': user['user_id'],
        'selling_price': 19.99,
        'stock': 100
    })
    productseller_id = response.json['productseller_id']

    # Now delete the product seller
    response = client.delete(f'{BASE_URL}/product-sellers/{productseller_id}')
    assert response.status_code == 204  # No Content

    # Verify deletion
    response = client.get(f'{BASE_URL}/product-sellers/{productseller_id}')
    assert response.status_code == 404  # Not Found

def test_get_sellers_by_product(client, init_data):
    user, productlist = init_data
    product = productlist[0]
    # Create a product seller
    client.post(f'{BASE_URL}/product-sellers', json={
        'product_id': product['product_id'],
        'seller_id': user['user_id'],
        'selling_price': 19.99,
        'stock': 100
    })
    product_id = product['product_id']
    response = client.get(f'{BASE_URL}/products/{product_id}/sellers')
    assert response.status_code == 200
    assert len(response.json) == 1  # There should be one seller for the product