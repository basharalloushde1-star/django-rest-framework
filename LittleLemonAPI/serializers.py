from rest_framework import serializers
from .models import MenuItem,Cart,Order,OrderItem
from django.contrib.auth.models import User,Group
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'password','username', 'email', 'groups']
class UserDeliverySerializer(serializers.ModelSerializer):
    groups_name = serializers.StringRelatedField(source='groups', many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'groups_name']

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        
       
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

       
        try:
            delivery_group = Group.objects.get(id=2)
            user.groups.add(delivery_group)
        except Group.DoesNotExist:
         
            pass
            
        return user
class CartSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),write_only=True
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), 
        write_only=True 
    )
   
    
    
  
    menu_details = MenuItemSerializer(source='menuitem', read_only=True)

    class Meta:
        model = Cart
       
        fields = ['user', 'menuitem', 'menu_details', 'quantity', 'unit_price', 'price']

from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True) # بجلب العناصر التابعة للطلب

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']