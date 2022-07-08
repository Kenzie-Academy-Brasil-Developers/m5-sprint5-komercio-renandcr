from products.serializers import CreateProductSerializer, ListProductSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from utils.mixins import CustomSerializerByMethodMixin

from products.permissions import CustomIsAnAuthorizedSeller, CustomIsTheResponsibleSeller
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from products.models import Product
from accounts.models import User

class ListCreateProductView(CustomSerializerByMethodMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, CustomIsAnAuthorizedSeller]
    queryset = Product.objects.all()

    serializer_map = {
        "GET": ListProductSerializer,
        "POST": CreateProductSerializer
    }

    def perform_create(self, serializer):
        return serializer.save(seller=User.objects.get(id=self.request.user.id))

class RetrieveUpdateProductView(CustomSerializerByMethodMixin, RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,CustomIsTheResponsibleSeller]
    queryset = Product.objects.all()
    
    serializer_map = {
        "GET": ListProductSerializer,
        "PATCH": CreateProductSerializer
    }

