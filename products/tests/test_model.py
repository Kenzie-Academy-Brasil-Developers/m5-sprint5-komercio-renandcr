from django.db import IntegrityError
from products.models import Product
from django.test import TestCase
from accounts.models import User

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email = "henry@gmail.com",
            first_name = "Tierry",
            last_name= "Henry",
            is_seller = True,
            password="123456"
        )

        cls.description = "Lorem Ipsu'm is simply dummy text of the printing and typesetting..."
        cls.price = 590.99
        cls.quantity = 2
        cls.is_active = True
        cls.seller = cls.user

        cls.product = Product(
            description = cls.description,
            price = cls.price,
            quantity = cls.quantity,
            is_active = cls.is_active,
        )

    def test_products_have_been_stored_correctly(self):
        self.product.seller = self.user
        self.product.save()
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertEqual(self.product.is_active, self.is_active)
        self.assertEqual(self.product.seller.id, self.seller.id)

    def test_active_is_the_default_true(self):
        product_instance = Product.objects.create(
                description = self.description,
                price = self.price,
                quantity = self.quantity,
                seller = self.user,
            )
        self.assertTrue(Product.objects.get(id=product_instance.id).is_active)


    def test_relationship_defined_in_creation(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                description = self.description,
                price = self.price,
                quantity = self.quantity,
                is_active = self.is_active,
            )

    def test_positive_integer_quantity(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                description = self.description,
                price = self.price,
                quantity = -1,
                is_active = self.is_active,
            )
    
    def test_user_can_have_multiple_products(self):
        products_instance_list = [Product(description=self.description,price=self.price,quantity=self.quantity) for _ in range(10)]
        for prod in products_instance_list:
            prod.seller = self.user

            prod.save()
        
        self.assertEqual(len(products_instance_list), self.user.products.count())


    



            














   