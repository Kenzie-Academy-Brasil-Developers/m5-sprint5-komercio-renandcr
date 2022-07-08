from rest_framework.test import APITestCase
from rest_framework.views import status
from accounts.models import User

class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller = {
            "email": "seller@gmail.com",
            "password": "123456",
            "first_name": "seller",
            "last_name": "seller",
            "is_seller": True
        }

        cls.user_default = {
            "email": "default@gmail.com",
            "password": "123456",
            "first_name": "default",
            "last_name": "default",
            "is_seller": False
        }

        cls.login = {
            "email": "seller@gmail.com",
            "password": "123456"
        }

            
    def test_seller_account_creator(self):
        """Usuário vendedor deve conseguir criar uma conta"""
        response = self.client.post("/api/accounts/", self.seller)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creator_account_not_seller(self):
        """Usuário não vendedor deve conseguir criar uma conta"""
        response = self.client.post("/api/accounts/", self.user_default)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_key_seller(self):
        """Requisição com nome de chave errada não é permitida ao usuário vendedor"""
        self.seller["emai"] = self.seller["email"]
        del self.seller["email"]
        response = self.client.post("/api/accounts/", self.seller)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_key_no_seller(self):
        """Requisição com nome de chave errada não é permitida ao usuário não vendedor"""
        self.user_default["emai"] = self.user_default["email"]
        del self.user_default["email"]
        response = self.client.post("/api/accounts/", self.user_default)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seller_login_returns_token(self):
        """Usuário vendedor deve retornar token no login"""
        seller = User.objects.create_user(**self.seller)
        response_token = self.client.post("/api/login/",self.login)
        self.assertEqual(seller.auth_token.key, response_token.data["token"])

    def test_login_not_seller_returns_token(self):
        """Usuário não vendedor deve retornar token no login"""
        user_default = User.objects.create_user(**self.user_default)
        response_token = self.client.post("/api/login/",self.user_default)
        self.assertEqual(user_default.auth_token.key, response_token.data["token"])

    def test_only_account_owner_updates_data(self):
        """Apenas usuário dono da conta altera seus dados"""
        self.client.force_authenticate(User.objects.create_user(**self.seller))
        user1_update_response = self.client.patch(f"/api/accounts/{1}/", {"first_name": "meu nome alterado"})
        self.assertEqual(user1_update_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(User.objects.create_user(**self.user_default))
        user2_update_response = self.client.patch(f"/api/accounts/{1}/", {"first_name": "nome de outro alterado"})
        self.assertEqual(user2_update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_disables_accounts(self):
        """Somente usuário administrador pode desativar outras contas"""
        self.client.force_authenticate(User.objects.create_superuser(**self.seller))
        user_default1 = User.objects.create_user(**self.user_default)
        user_admin_deactivate_response = self.client.patch(f"/api/accounts/{user_default1.id}/management/", {"is_active": False})
        self.assertEqual(user_admin_deactivate_response.status_code, status.HTTP_200_OK)

        user_admin_activate_response = self.client.patch(f"/api/accounts/{user_default1.id}/management/", {"is_active": True})
        self.assertEqual(user_admin_activate_response.status_code, status.HTTP_200_OK)
 
        self.user_default["email"] = "default2@gmail.com"
        self.client.force_authenticate(User.objects.create_user(**self.user_default))
        user_default_deactivate_response = self.client.patch(f"/api/accounts/{user_default1.id}/management/", {"is_active": False})
        self.assertEqual(user_default_deactivate_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_everyone_can_list_users(self):
        User.objects.create_user(**self.user_default)
        user_get_response = self.client.get("/api/accounts/")
        self.assertEqual(user_get_response.status_code, status.HTTP_200_OK) 










