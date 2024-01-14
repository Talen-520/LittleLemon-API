from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from .serializers import MenuItemSerializer,CartSerializer,UserSerializer,OrderSerializer  
from .models import Cart, MenuItem, Order,OrderItem
from rest_framework.throttling import AnonRateThrottle 
from rest_framework.throttling import UserRateThrottle 
from rest_framework.decorators import throttle_classes
from .throttles import  TenCallsPerMinute # import file

# Menu-items endpoints
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            items = MenuItem.objects.select_related('category').all() 
            category_name = request.query_params.get('category')
            to_price = request.query_params.get('to_price')
            search = request.query_params.get('search')
            ordering = request.query_params.get('ordering')
            perpage = request.query_params.get('perpage',default=2)
            page = request.query_params.get('page',default=1)
            #fliter , sorting, search
            if category_name:  
                items = items.filter(category__title=category_name)
            if to_price:  
                items = items.filter(price__lte=to_price) 
            if search:
                items = items.filter(title__icontains=search) 
            if ordering:  
                ordering_fields = ordering.split(',')
                items = items.order_by(*ordering_fields) 

            paginator = Paginator(items,per_page=perpage)
            try:
                items = paginator.page(number = page)
            except EmptyPage:
                items = []
            serialized_item = MenuItemSerializer(items, many=True)  
            return Response(serialized_item.data)
        if request.method == 'POST':
            serialized_item = MenuItemSerializer(data=request.data) 
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data,status=status.HTTP_201_CREATED)
    else: #customer
        if request.method == 'GET':
            items = MenuItem.objects.all()
            serialized_item = MenuItemSerializer(items, many=True) 
            return Response(serialized_item.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_item(request, pk):
    # Retrieve the menu item or return 404 if not found
    item = get_object_or_404(MenuItem, pk=pk)
    
    # Managers can update or delete the item
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'PUT':
            # Logic for updating the item
            serializer = MenuItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            # Logic for partially updating the item
            serializer = MenuItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            # Logic for deleting the item
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    # All authenticated users can view the item
    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)
    
    # If a user who is not a manager tries to PUT, PATCH, or DELETE, return unauthorized
    return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)


# Djoser manager Group add/delete user
# Helper function to check if a user is in the manager group
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manager_group_users(request, user_id=None):
    # Check if the user making the request is a manager
    if not is_manager(request.user):
        return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    manager_group = Group.objects.get(name='Manager')

    if request.method == 'GET':
        # Return all users in the manager group
        managers = manager_group.user_set.all()
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Assign the user in the payload to the manager group
        user = get_object_or_404(User, username=request.data.get('username'))
        manager_group.user_set.add(user)
        return Response({"message": "User added to manager group successfully."}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        # Remove the specified user from the manager group
        user = get_object_or_404(User, pk=user_id)
        manager_group.user_set.remove(user)
        return Response({"message": "User removed from manager group successfully."}, status=status.HTTP_200_OK)

    return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew_users(request, user_id=None):
    # Ensure the user making the request is a manager
    if not is_manager(request.user):
        return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    delivery_crew_group = Group.objects.get(name='Delivery Crew')

    if request.method == 'GET':
        # Return all users in the delivery crew group
        delivery_crew = delivery_crew_group.user_set.all()
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Add user to the delivery crew group
        user = get_object_or_404(User, username=request.data.get('username'))
        delivery_crew_group.user_set.add(user)
        return Response({"message": "User added to delivery crew group successfully."}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        # Remove user from the delivery crew group
        user = get_object_or_404(User, pk=user_id)
        delivery_crew_group.user_set.remove(user)
        return Response({"message": "User removed from delivery crew group successfully."}, status=status.HTTP_200_OK)

    return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#Cart management endpoints 

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_management(request):
    if request.method == 'GET':
        # Retrieve all cart items for the current user
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        # Add a new item to the cart for the current user
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity', 1)
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        # Create a new cart item
        cart_item = Cart.objects.create(
            user=request.user,
            menuitem=menu_item,
            quantity=quantity,
            unit_price=menu_item.price,  # Assume unit_price is the same as the menu item price
            price=menu_item.price * quantity  # Total price based on quantity
        )
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == 'DELETE':
        # Delete all cart items for the current user
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


#Order management endpoints
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

# Helper function to check if a user is part of the delivery crew
def is_delivery_crew(user):
    return user.groups.filter(name='Delivery Crew').exists()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_list(request):
    if request.method == 'GET':
        # Customers see their orders, managers see all orders
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create an order from the user's cart items
        with transaction.atomic():
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                return Response({'detail': 'No items in cart.'}, status=status.HTTP_400_BAD_REQUEST)
            
            order = Order.objects.create(user=request.user)  # Set other fields as needed
            order_items = [
                OrderItem(order=order, menuitem=cart_item.menuitem, quantity=cart_item.quantity,
                          unit_price=cart_item.unit_price, price=cart_item.price)
                for cart_item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()  # Clear the cart
            return Response({'detail': 'Order created.'}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'GET':
        # Check ownership or manager status
        if order.user != request.user and not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        # Allow updates by managers or delivery crew (for status updates)
        if request.user.is_staff or (is_delivery_crew(request.user) and 'status' in request.data):
            serializer = OrderSerializer(order, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE' and request.user.is_staff:
        # Allow deletion by managers only
        order.delete()
        return Response({'detail': 'Order deleted.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])

def delivery_orders(request, order_id=None):
    if request.method == 'GET' and is_delivery_crew(request.user):
        # Delivery crew can view their assigned orders
        orders = Order.objects.filter(delivery_crew=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'PATCH' and order_id and is_delivery_crew(request.user):
        # Delivery crew can update the status of their assigned orders
        order = get_object_or_404(Order, id=order_id, delivery_crew=request.user)
        status = request.data.get('status')
        if status in ['0', '1']:  # Check if status is valid
            order.status = status
            order.save(update_fields=['status'])
            return Response({'detail': 'Order status updated.'})
        return Response({'detail': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
