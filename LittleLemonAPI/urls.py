from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #customer
    #path('menu-items/',views.MenuItemView.as_view()),
    #path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),

    # Menu-items endpoints

    path('menu_items/',views.menu_items),
    path('menu_items/<int:pk>',views.single_item),

    #User group management endpoints
    path('groups/manager/users', views.manager_group_users),
    path('groups/manager/users/<int:user_id>/', views.manager_group_users),#test with get post delete with http://127.0.0.1:8000/api/groups/delivery-crew/users/3/
    path('groups/delivery-crew/users', views.delivery_crew_users),
    path('groups/delivery-crew/users/<int:user_id>/', views.delivery_crew_users), #test with get post delete with http://127.0.0.1:8000/api/groups/delivery-crew/users/3/

    # Cart management endpoints 
    path('cart/menu-items', views.cart_management), 

    #Order management endpoints
    path('orders', views.order_list, name='order-list'),
    path('orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('orders/<int:order_id>/delivery', views.delivery_orders, name='delivery-order-update'),

]