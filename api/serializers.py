from rest_framework import serializers
from .models import Product, Order, OrderItem

# ProductSerializer: Handles serialization for the Product model.
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'description',
            'stock',
        )

    # validate_price: Custom validator to ensure that the price is greater than zero.
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# OrderItemSerializer: Handles serialization for OrderItem model.
class OrderItemSerializer(serializers.ModelSerializer):
    # Fetching and displaying product details through nested data.
    # product = ProductSerializer(read_only=True)  # Example of full product serialization commented out.
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    
    class Meta:
        model = OrderItem
        fields = (
            # 'product',  # Uncomment to serialize full product details.
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )

# OrderSerializer: Handles serialization for the Order model with nested serialization for order items.

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # Nested serializer for handling multiple OrderItems linked to an Order.

    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
        # Calculate total price of the order by summing up all the item subtotals.
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



class ProductInfoSerializer(serializers.Serializer):
    # Serializer for gathering product information: list of products, count, and maximum price.
    products = ProductSerializer(many=True)  # Serializing multiple products.
    count = serializers.IntegerField()  # Total count of products.
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)  # Maximum price among the products.



# serializers convert python data types into json data

# serializer_fields converting between primitive values and internal data types, they also deal with validating input values, as well as retrieving and setting the values from thier parent objects
    
    
    

