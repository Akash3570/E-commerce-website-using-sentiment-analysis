from import_export import resources
from .models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'description', 'image')
        export_order = ('id', 'name', 'price', 'category', 'description', 'image')
