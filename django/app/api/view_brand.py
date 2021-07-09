from rest_framework import viewsets
from .models import Brand
from .serializer_brand import BrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()