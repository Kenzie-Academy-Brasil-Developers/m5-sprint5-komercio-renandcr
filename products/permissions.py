from django.shortcuts import get_list_or_404
from rest_framework import permissions
from products.models import Product

class CustomIsAnAuthorizedSeller(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_seller

class CustomIsTheResponsibleSeller(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in permissions.SAFE_METHODS:
            return True
        product_parameter_id = request.__dict__["parser_context"]["kwargs"]["pk"]
        product_instance = get_list_or_404(Product, pk=product_parameter_id)[0] 

        return request.user.id == product_instance.seller.id 