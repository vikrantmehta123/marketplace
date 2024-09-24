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
        'roles': [2]  # Example roles
    })
    seller = user_response.get_json()

    user_response = client.post(f'{BASE_URL}/users', json={
        'username': 'jane_doe',
        'email': 'jane@example.com',
        'password': 'securepassword',
        'contact': '1234567890',
        'address': '123 Main St',
        'roles': [3]  # Example roles
    })

    buyer = user_response.get_json()

    datalist = [
        {
            'product_name': 'Product1',
            'description': 'Product Description1',
            'category_id': 1,
            'created_by': 1
        },
        {
            'product_name': 'Product2',
            'description': 'Product Description3',
            'category_id': 1,
            'created_by': 1
        }
    ]

    data_responses = []
    for data in datalist:
        response = client.post(f'{BASE_URL}/products', json=data)
        data_responses.append(response.get_json())
    return buyer, seller, data_responses

def test_create_order(client, init_data):
    buyer, seller, product = init_data
    seller_id = seller['user_id']
    # Test creating an order
    response = client.post(f'{BASE_URL}/orders', json={
        'buyer_id': buyer['user_id'],
        
        'items': [
            {'seller_id': seller_id, 'product_id': 1, 'price': 100.0, 'quantity': 2},
            {'seller_id': seller_id, 'product_id': 2, 'price': 150.0, 'quantity': 1},
        ]
    })
    assert response.status_code == 201  # Created
    data = response.get_json()
    assert 'order_id' in data  # Ensure order ID is returned

def test_get_order(client, init_data):
    buyer, seller, product = init_data
    seller_id = seller['user_id']
    # First create an order
    response = client.post(f'{BASE_URL}/orders', json={
        'buyer_id': buyer['user_id'],
        'items': [
            {'seller_id': seller_id, 'product_id': product[0]['product_id'], 'price': 100.0, 'quantity': 2},
        ]
    })
    order_id = response.get_json()['order_id']

    # Test retrieving the created order
    response = client.get(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 200  # OK
    data = response.get_json()
    assert data['buyer_id'] == buyer['user_id'] # Verify buyer ID

def test_delete_order(client, init_data):
    buyer, seller, product = init_data
    seller_id = seller['user_id']
    # Create an order
    response = client.post(f'{BASE_URL}/orders', json={
        'buyer_id': buyer['user_id'],
        'items': [{'seller_id': seller_id, 'product_id': product[0]['product_id'], 'price': 100.0, 'quantity': 2}]
    })
    order_id = response.get_json()['order_id']

    response = client.get(f'{BASE_URL}/orders/{order_id}')

    # Test deleting the created order
    response = client.delete(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 204  # No Content

    # Verify that the order no longer exists
    response = client.get(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 404  # Not found
