import pytest

BASE_URL = "http://127.0.0.1:5000/api/v1"

@pytest.fixture
def preinsertions(client):
    client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    client.post(f'{BASE_URL}/category', json={'name': 'Home Appliances'})
    client.post(f'{BASE_URL}/users', json={
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'securepassword',
        'contact': '1234567890',
        'address': '123 Main St',
        'roles': [1, 2, 3]  # Example roles
    })
    return


@pytest.fixture
def product_insertions(client, preinsertions):
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

    lastinserted_product = None
    for data in datalist:
        response = client.post(f'{BASE_URL}/products', json=data)
        lastinserted_product = response.get_json()
    return lastinserted_product

def test_create_product(client, preinsertions):
    data = {
        'product_name': 'New Product',
        'description': 'New Product Description',
        'category_id': 1,
        'created_by': 1
    }
    response = client.post(f'{BASE_URL}/products', json=data)
    assert response.status_code == 201
    assert response.json['product_name'] == 'New Product'


def test_get_products_by_category_id(client, preinsertions, product_insertions):
    response = client.get(f"{BASE_URL}/products", json={'category_id':1})
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == 404

def test_update_product(client, product_insertions):
    data = {
        'product_name': 'Updated Product',
        'description': 'Updated Description'
    }
    product_id = product_insertions['product_id']

    response = client.put(f'{BASE_URL}/products/{product_id}', json=data)
    assert response.status_code == 200
    assert response.json['product_name'] == 'Updated Product'
