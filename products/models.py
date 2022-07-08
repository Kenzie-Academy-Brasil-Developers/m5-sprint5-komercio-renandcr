from django.db import models

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="products")

    def __repr__(self) -> str:
        return f"model:Product - id:{self.id} - seller_id:{self.seller_id}"