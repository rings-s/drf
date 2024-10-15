from rest_framework import serializers
from .models import Product, Order, OrderItem



class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'description',
            'stock',
        
        )
        
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class OrderSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Order
        fields = '__all__'
        




    # serializers convert python data types into json data

    # serializer_fields converting between primitive values and internal data types, they also deal with validating input values, as well as retrieving and setting the values from thier parent objects
    
    
    
