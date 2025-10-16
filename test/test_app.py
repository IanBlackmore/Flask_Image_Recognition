# test_integration_happy.py

from io import BytesIO
import pytest

def test_load_home_page(client):
    """Test if home page can be loaded successfully."""
    response = client.get("/",)
    assert response.status_code == 200
    assert b"Hand Sign Digit Language Detection" in response.data 

def test_load_prediction_page(client):
    """Test if prediction page can be loaded successfully."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.jpg"
    response = client.post("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"Prediction" in response.data 

def test_valid(client):
    """Test if prediction page can be loaded successfully."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.img"
    response = client.post("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data 

def test_invalid_file(client):
    """Test if app can process image."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.pdf"
    response = client.post("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data 

def test_large_file(client):
    """Test if app can process large file."""
    img_data = BytesIO(b"fake_image_data" * 100 * 100)
    img_data.name = "test.img"
    response = client.post("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data 

def test_non_standard_extension(client):
    """Test if app can process non standard extension image file."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.webp"
    response = client.post("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data 

def test_incorrect_method_1(client):
    """Test if API endpoint return 405 for incorrect method."""
    response = client.post("/",)
    assert response.status_code == 405

def test_incorrect_method_2(client):
    """Test if API endpoint return 405 for incorrect method."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.jpg"
    response = client.get("/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data")
    assert response.status_code == 405
