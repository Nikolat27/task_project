from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product

User = get_user_model()


class ProductsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user_name",
            password="test_user_pass",
            email="test@gmail.com",
        )
        self.token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.product = Product.objects.create(
            name="Test Product1", created_by=self.user, price=1111
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_create_product(self):
        initial_count = Product.objects.count()
        data = {"name": "New Product", "price": 123, "created_by": self.user.id}
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_count + 1)

    def test_update_product(self):  # If not authorized it returns 401 error
        new_name = "Updated Product"
        data = {"name": new_name}
        response = self.client.put(f"/api/products/{self.product.id}/", data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # If not authorized it returns 401 error
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, new_name)

    def test_delete_product(self):
        initial_count = Product.objects.count()
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), initial_count - 1)

    def test_update_product_unauthorized(self):
        another_user = self.create_user(
            "random_user", "random_pass", "random@gmail.com"
        )
        self.client.credentials()  # Remove the first user's token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_token(another_user)}"
        )

        update_name = "Try to update"
        data = {"name": update_name}
        response = self.client.put(f"/api/products/{self.product.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_unauthorized(self):
        another_user = self.create_user("random_user", "random_pass", "random@gmail.com")
        self.client.credentials()  # Remove the first user's token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_token(another_user)}"
        )

        # Attempt to delete the product created by self.user
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_user(self, username, password, email):
        return User.objects.create_user(
            username=username, password=password, email=email
        )
