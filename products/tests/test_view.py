from rest_framework.test import APITestCase
from rest_framework.views import status
from django.db import IntegrityError 
from products.models import Product
from accounts.models import User

class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = {
            "email": "seller@gmail.com",
            "password": "123456",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": True
        }
        cls.seller_data2 = {
            "email": "seller2@gmail.com",
            "password": "123456",
            "first_name": "seller2",
            "last_name": "seller2",
            "is_seller": True
        }

        cls.user_default_data = {
            "email": "user_default@gmail.com",
            "password": "123456",
            "first_name": "default",
            "last_name": "default",
            "is_seller": False
        }

        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
            "is_active": True
        }

    def test_only_seller_creates_product(self):
        """Somente vendedor pode criar produtos"""
        self.client.force_authenticate(User.objects.create_user(**self.seller_data))
        seller_create_product_response = self.client.post("/api/products/", self.product_data)
        self.assertEqual(seller_create_product_response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(User.objects.create_user(**self.user_default_data))
        user_default_create_response = self.client.post("/api/products/", self.product_data)
        self.assertEqual(user_default_create_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_seller_updates_product(self):
        """Somente o vendedor associado ao produto pode atualizá-lo."""
        self.client.force_authenticate(User.objects.create_user(**self.seller_data))
        product_response = self.client.post("/api/products/", self.product_data)
        seller1_update_response = self.client.patch(f"/api/products/{product_response.data['id']}/", self.product_data)
        self.assertEqual(seller1_update_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(User.objects.create_user(**self.seller_data2))
        seller2_update_response = self.client.patch(f"/api/products/{product_response.data['id']}/", self.product_data)
        self.assertEqual(seller2_update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_everyone_can_list_and_filter_product(self):
        """Qualquer um pode listar e filtrar produtos."""
        user = User.objects.create(**self.seller_data)
        product = Product.objects.create(**self.product_data, seller=user)
        retrieve_response = self.client.get(f"/api/products/{product.id}/")
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        list_response = self.client.get("/api/products/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_wrong_key(self):
        """Verificar se as chaves foram enviadas corretamente"""
        self.client.force_authenticate(User.objects.create_user(**self.seller_data))
        self.product_data["pric"] = self.product_data["price"] 
        del self.product_data["price"]
        product_response = self.client.post("/api/products/", self.product_data)
        self.assertEqual(product_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_negative_quantity(self):
        """Não deve ser possível criar produtos com quantidade negativa."""
        self.client.force_authenticate(User.objects.create_user(**self.seller_data))
        self.product_data["quantity"] = -1
        with self.assertRaises(IntegrityError):
            self.client.post("/api/products/", self.product_data)
            
    def test_specific_return_on_creation_and_listing(self):
        """Retorno específico para listagem e criação."""
        self.client.force_authenticate(User.objects.create_user(**self.seller_data))
        create_response = self.client.post("/api/products/", self.product_data, format="json")
        
        expected_return_create = {
            "id": create_response.data['id'],
		    "seller": {
                "id": create_response.data['seller']['id'],
                "email": "seller@gmail.com",
                "first_name": "seller",
                "last_name": "seller",
                "is_seller": True,
                "date_joined": f"{create_response.data['seller']['date_joined']}"
                
            },
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
                "is_active": True,
	    }

        expected_return_listing = [{
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
            "is_active": True,
            "seller": create_response.data['seller']['id']
        }]

        self.assertEqual(expected_return_create, create_response.json())
    
        listing_response = self.client.get("/api/products/", format="json")
        self.assertEqual(expected_return_listing, listing_response.json())
       
