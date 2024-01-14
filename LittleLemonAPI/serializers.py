from rest_framework import serializers
from .models import MenuItem
from .models import Category
from .models import Cart
from .models import Order
from .models import OrderItem
from decimal import Decimal 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title'] 

class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax') #to display price after tax
    category = CategorySerializer(read_only=True)   
    category_id = serializers.IntegerField(write_only=True)  
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','price_after_tax','category','category_id']
    def calculate_tax(self,product:MenuItem): 
        return product.price * Decimal(1.1)

class CartSerializer(serializers.ModelSerializer):
    # Nested serializer for the menuitem
    menuitem = MenuItemSerializer(read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew','status','total','data']