from rest_framework import generics,filters
from .models import MenuItem,Cart,OrderItem,Order
from .serializers import MenuItemSerializer,UserSerializer,UserDeliverySerializer,CartSerializer,OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


all_users = User.objects.all()

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    
    filterset_fields = {
        'price': ['gte', 'lte'],    
        'category__title': ['exact'],
    }
    
    
    search_fields = ['title', 'category__title']
    
    
    ordering_fields = ['price', 'inventory']
    def post(self, request, *args, **kwargs):
        user=self.request.user
        if user.groups.filter(name='Delivery crew').exists() or not request.user.groups.exists():
            return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
        elif user.groups.filter(name='Manager'):
         return super().post(request, *args, **kwargs)
class MenuSingleItemView(generics.RetrieveUpdateDestroyAPIView):
   queryset = MenuItem.objects.all()
   serializer_class = MenuItemSerializer
   permission_classes=[IsAuthenticated]
   def retrieve(self, request, *args, **kwargs):
    
      return super().retrieve(request, *args, **kwargs)
   def update(self, request, *args, **kwargs):
      user=self.request.user
      if user.groups.filter(name='Delivery crew').exists() or not request.user.groups.exists():
            return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
      elif user.groups.filter(name='Manager'):
         return super().update(request, *args, **kwargs)
   
   def destroy(self, request, *args, **kwargs):
      user=self.request.user
      if user.groups.filter(name='Delivery crew').exists() or not request.user.groups.exists():
            return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
      elif user.groups.filter(name='Manager'):
         return super().destroy(request, *args, **kwargs)
class UsersView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=User.objects.filter(groups__name='Manager')
    serializer_class=UserSerializer
    def get(self, request, *args, **kwargs):
        user=self.request.user
        if user.groups.filter(name='Manager'):
         return super().get(request, *args, **kwargs)
        else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request, *args, **kwargs):
        user=self.request.user
        if user.groups.filter(name='Manager'):
         return super().post(request, *args, **kwargs)
        else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
class SingleUserDeleteView(generics.DestroyAPIView):
   queryset=User.objects.filter(groups__name='Manager')
   serializer_class=UserSerializer
   def destroy(self, request, *args, **kwargs):
      user=self.request.user
      if user.groups.filter(name='Manager'):
       return super().destroy(request, *args, **kwargs)
      else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
class UserDeliveryView(generics.ListCreateAPIView):
   permission_classes=[IsAuthenticated]
   queryset=User.objects.filter(groups__name='Delivery crew')
   serializer_class=UserDeliverySerializer
   def get(self, request, *args, **kwargs):
        user=self.request.user
        if user.groups.filter(name='Manager'):
         return super().get(request, *args, **kwargs)
        else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
   def post(self, request, *args, **kwargs):
        user=self.request.user
        if user.groups.filter(name='Manager'):
         return super().post(request, *args, **kwargs)
        else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
class UserDeliveryDeleteView(generics.DestroyAPIView):
   permission_classes=[IsAuthenticated]
   queryset= User.objects.filter(groups__name='Delivery crew')
   serializer_class=UserDeliverySerializer
   def destroy(self, request, *args, **kwargs):
      user=self.request.user
      if user.groups.filter(name='Manager'):
       return super().destroy(request, *args, **kwargs)
      else:
         return Response(
            {"detail": "you don't have access"}, 
            status=status.HTTP_401_UNAUTHORIZED)
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        
        cart_items = self.get_queryset()
        
        if cart_items.exists():
            cart_items.delete()
            return Response(
                {"message":'all items are deleted'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        
        return Response(
            {"message":"the cart is already empty"}, 
            status=status.HTTP_404_NOT_FOUND
        )


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    
    filterset_fields = ['status', 'date']
    
    
    search_fields = ['user__username']
    
    
    ordering_fields = ['total', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user) 
        else:
            return Order.objects.filter(user=user) 

    def create(self, request, *args, **kwargs):
        
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"message":"the cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    
        total = sum(item.price for item in cart_items)

      
        order = Order.objects.create(user=request.user, total=total, status=False)

        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        
     
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        
        if request.user.groups.filter(name='Manager').exists():
            return super().delete(request, *args, **kwargs)
        return Response({"message": "the current user is not allowed to delete the order"}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if user.groups.filter(name='Manager').exists():
            if 'delivery_crew' in request.data:
                order.delivery_crew_id = request.data['delivery_crew']
            if 'status' in request.data:
                order.status = request.data['status']
            order.save()
            return Response({"message":"updated by the  manager"})

       
        if user.groups.filter(name='Delivery Crew').exists():
            if order.delivery_crew == user:
                if 'status' in request.data:
                    
                    order.status = request.data['status']
                    order.save()
                    return Response({"message": "updated by the delivery crew"})
            return Response({"message": "you cannot edit an order that is not yours"}, status=status.HTTP_403_FORBIDDEN)
            
        return Response({"message": "you are not authorized"}, status=status.HTTP_403_FORBIDDEN)
   
        