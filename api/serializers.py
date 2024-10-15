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
    # product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    class Meta:
        model = OrderItem
        fields = (
            # 'product',
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
            
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
    
    
    
