BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_create_category(client):
    # Test creating a new category
    response = client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['category_name'] == 'Electronics'

def test_get_category(client):
    response = client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    response = client.get(f'{BASE_URL}/category/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['category_name'] == 'Electronics'

def test_update_category(client):
    # Test updating the category
    client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    response = client.put(f'{BASE_URL}/category/1', json={'name': 'Home Appliances'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['category_name'] == 'Home Appliances'

def test_delete_category(client):
    # Test deleting the category
    client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    response = client.delete(f'{BASE_URL}/category/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Category deleted successfully"

def test_category_not_found(client):
    # Test getting a category that does not exist
    response = client.get(f'{BASE_URL}/category/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Category not found"

def test_get_all_categories(client):
    client.post(f'{BASE_URL}/category', json={'name': 'Electronics'})
    client.post(f'{BASE_URL}/category', json={'name': 'Home Appliances'})

    response = client.get(f"{BASE_URL}/category")
    data = response.get_json()
    assert len(data) == 2
    assert isinstance(data, list)

    assert 'category_name' in data[0]
    assert 'category_name' in data[1]