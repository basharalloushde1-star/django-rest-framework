from django.contrib import admin
from django.urls import path
from .views import MenuItemsView,MenuSingleItemView,UsersView,SingleUserDeleteView,UserDeliveryView,UserDeliveryDeleteView,CartView,OrderView,SingleOrderView



urlpatterns=[

    
    path('menu-items/',MenuItemsView.as_view()),
   # urls.py

    path('menu-items/<int:pk>/', MenuSingleItemView.as_view()),
    path('groups/manager/users/',UsersView.as_view()),
    path('groups/groups/manager/users/<int:pk>',SingleUserDeleteView.as_view()),
    path('groups/delivery-crew/users/',UserDeliveryView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/',UserDeliveryDeleteView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/',UserDeliveryDeleteView.as_view()),
    path('cart/menu-items/',CartView.as_view()),
    path('orders/',OrderView.as_view()),
    path('orders/<int:pk>/',SingleOrderView.as_view()),


]