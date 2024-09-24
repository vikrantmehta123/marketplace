from application.dal import *
import os
import sys
BASE_URL = "http://127.0.0.1:5000/api/v1"

# Ensure the backend directory is in the system path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))


def test_create_user(client):
    response = client.post(f'{BASE_URL}/users', json={
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'securepassword',
        'contact': '1234567890',
        'address': '123 Main St',
        'roles': [2]  # Example roles
    })
    assert response.status_code == 201
    # Assuming the response contains user_id
    assert 'user_id' in response.get_json()


def test_get_user_by_id(client):
    # Create a user first
    user_created_response = client.post(f'{BASE_URL}/users', json={
        'username': 'jane_doe',
        'email': 'jane@example.com',
        'password': 'securepassword',
        'contact': '0987654321',
        'address': '456 Elm St',
        'roles': [2]
    })

    user_id = user_created_response.get_json()['user_id']

    response = client.get(f'{BASE_URL}/users/{user_id}')

    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'jane_doe'


def test_get_user_by_username(client):
    # Create a user first
    user_created_response = client.post(f'{BASE_URL}/users', json={
        'username': 'jane_doe',
        'email': 'jane@example.com',
        'password': 'securepassword',
        'contact': '0987654321',
        'address': '456 Elm St',
        'roles': [2]
    })

    username = user_created_response.get_json()['username']

    response = client.get(f'{BASE_URL}/users/{username}')

    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'jane_doe'


def test_update_user(client):
    user_created_response = client.post(f'{BASE_URL}/users', json={
        'username': 'jane_doe',
        'email': 'jane@example.com',
        'password': 'securepassword',
        'contact': '0987654321',
        'address': '456 Elm St',
        'roles': [2]
    })

    user_id = user_created_response.get_json()['user_id']

    response = client.put(f'{BASE_URL}/users/{user_id}', json={
        'contact': '9876543210',
        'address': '789 Maple St'
    })

    print(response.text)
    assert response.status_code == 200
    updated_user = UserDAL.get_user_by_id(user_id=user_id)
    assert updated_user.contact == '9876543210'
    assert updated_user.address == '789 Maple St'
