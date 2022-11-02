def test_get_all_breakky_empty_with_empty_list(client):
    # Act
    response = client.get("/breakfast")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_breakfast_no_db(client):
    response = client.get("/breakfast/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 418
    assert "message" in response_body

def test_get_one_existing_breakfast(client, two_breakfasts):
    response = client.get('breakfast/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {'id': 1, 'name': 'Cheese Omelet', 'prep_time': 25, 'rating': 4.0}

def test_get_one_nonexisting_breakfast(client, two_breakfasts):
    response = client.get('breakfast/100')
    response_body = response.get_json()

    assert response.status_code == 418
    assert "message" in response_body

def test_get_one_invalid_breakfast(client):
    response = client.get('breakfast/hello')
    response_body = response.get_json()

    assert response.status_code == 400
    assert "message" in response_body