import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from starlette import status

from app import main
from app.serializers import schemas


class TestProductManagement(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def tearDown(self):
        self.client = None

    @patch("app.crud.get_all_products")
    def test_read_all_products(self, mock_get_all_products):
        mock_get_all_products.return_value = [
            schemas.Product(
                id=1,
                name="Product 1",
                description="Description 1",
                price=10,
                quantity=5,
                category="Category 1",
            ),
            schemas.Product(
                id=2,
                name="Product 2",
                description="Description 2",
                price=20,
                quantity=10,
                category="Category 2",
            ),
        ]
        response = self.client.get("/products/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    @patch("app.crud.get_product_by_id")
    def test_read_product(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = schemas.Product(
            id=1,
            name="Product 1",
            description="Description 1",
            price=10,
            quantity=5,
            category="Category 1",
        )
        response = self.client.get("/products/1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Product 1")

    @patch("app.crud.create_product")
    def test_create_product(self, mock_create_product):
        mock_create_product.return_value = schemas.Product(
            id=1,
            name="New Product",
            description="New Description",
            price=15,
            quantity=3,
            category="New Category",
        )
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 15,
            "quantity": 3,
            "category": "New Category",
        }
        response = self.client.post("/products/", json=product_data)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "New Product")

    @patch("app.crud.update_product")
    def test_update_product(self, mock_update_product):
        mock_update_product.return_value = schemas.Product(
            id=1,
            name="Updated Product",
            description="Updated Description",
            price=20,
            quantity=7,
            category="Updated Category",
        )
        product_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 20,
            "quantity": 7,
            "category": "Updated Category",
        }
        response = self.client.put("/products/1", json=product_data)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Product")

    @patch("app.crud.delete_product")
    def test_delete_product(self, mock_delete_product):
        mock_delete_product.return_value = True
        response = self.client.delete("/products/1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Product deleted")

    def test_update_product_invalid_data(self):
        product_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": "Invalid Price",
            "quantity": 10,
            "category": "Updated Category",
        }
        response = self.client.put("/products/1", json=product_data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertEqual(data["detail"][0]["loc"], ["body", "price"])

    @patch("app.crud.get_product_by_id")
    def test_read_product_not_found(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = None
        response = self.client.get("/products/999")
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["detail"], "Product not found")

    @patch("app.crud.update_product")
    def test_update_product_not_found(self, mock_update_product):
        mock_update_product.return_value = None
        product_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 20,
            "quantity": 7,
            "category": "Updated Category",
        }
        response = self.client.put("/products/999", json=product_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["detail"], "Product not found")

    @patch("app.crud.delete_product")
    def test_delete_product_not_found(self, mock_delete_product):
        mock_delete_product.return_value = False
        response = self.client.delete("/products/999")
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["detail"], "Product not found")

    @patch("app.crud.get_all_products")
    def test_read_all_products_empty(self, mock_get_all_products):
        mock_get_all_products.return_value = []
        response = self.client.get("/products/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    @patch("app.crud.create_product")
    def test_create_product_invalid_data(self, mock_create_product):
        mock_create_product.return_value = None
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": "Invalid Price",
            "quantity": 3,
            "category": "New Category",
        }
        response = self.client.post("/products/", json=product_data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertEqual(data["detail"][0]["loc"], ["body", "price"])
