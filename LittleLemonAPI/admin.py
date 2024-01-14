from django.contrib import admin
from .models import Category
from .models import MenuItem
from .models import Cart
from .models import Order
from .models import OrderItem
# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
