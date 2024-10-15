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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            
        )

# nested serializer
class OrderSerializer(serializers.ModelSerializer):
    # nested serializer
    items = OrderItemSerializer(many=True, read_only=True) 
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
            )
        
        




    # serializers convert python data types into json data

    # serializer_fields converting between primitive values and internal data types, they also deal with validating input values, as well as retrieving and setting the values from thier parent objects
    
    
    
