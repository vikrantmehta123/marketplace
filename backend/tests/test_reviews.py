import pytest

BASE_URL = "http://127.0.0.1:5000/api/v1"


@pytest.fixture
def create_products(client):
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

def test_create_review(client, create_products):
    response = client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 4.5,
        'comment': "Great product!"
    })
    assert response.status_code == 201
    assert 'review_id' in response.get_json()  # Ensure review ID is returned

def test_get_review(client, create_products):
    # Create a review first
    review_response = client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 4.5,
        'comment': "Great product!"
    })
    review_id = review_response.get_json()['review_id']

    response = client.get(f"{BASE_URL}/reviews/{review_id}")
    assert response.status_code == 200
    assert response.get_json()['rating'] == 4.5

def test_get_review_not_found(client):
    response = client.get(f"{BASE_URL}/reviews/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404

def test_get_reviews_by_product(client, create_products):
    # Create a review for the product first
    client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 4.5,
        'comment': "Great product!"
    })

    client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 5,
        'comment': "Amazing product!"
    })

    response = client.get(f"{BASE_URL}/products/1/reviews")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)  # Should return a list of reviews
    assert len(response.get_json()) == 2

def test_update_review(client, create_products):
    # Create a review first
    review_response = client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 4.5,
        'comment': "Great product!"
    })
    review_id = review_response.get_json()['review_id']
    
    response = client.put(f"{BASE_URL}/reviews/{review_id}", json={
        'rating': 5.0,
        'comment': "Amazing product!"
    })

    assert response.status_code == 200
    assert response.get_json()['rating'] == 5.0

def test_update_review_not_found(client, create_products):
    response = client.put(f"{BASE_URL}/reviews/9999", json={
        'rating': 5.0,
        'comment': "Amazing product!"
    })
    assert response.status_code == 404

def test_delete_review(client, create_products):
    # Create a review first
    review_response = client.post(f"{BASE_URL}/reviews", json={
        'user_id': 1,
        'product_id': 1,
        'rating': 4.5,
        'comment': "Great product!"
    })
    review_id = review_response.get_json()['review_id']

    response = client.delete(f"{BASE_URL}/reviews/{review_id}")
    assert response.status_code == 204

    # Check if the review is indeed deleted
    response = client.get(f"{BASE_URL}/reviews/{review_id}")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Review not found'

def test_delete_review_not_found(client):
    response = client.delete(f"{BASE_URL}/reviews/9999")  # Assuming this ID doesn't exist
    assert response.status_code == 404