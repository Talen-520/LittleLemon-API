from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,db_index = True) # client application will search against this title field so index it
    def __str__(self):
        return f"{self.title}"

class MenuItem(models.Model):
    title = models.CharField(max_length=255,db_index = True)
    price = models.DecimalField(max_digits=6, decimal_places=2,db_index = True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT) 
    def __str__(self):
        return f"{self.title}"
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta: #only one menu item for specific user, you can only change quantity of menuitem
        unique_together = ('user', 'menuitem')
    def __str__(self):
        return f"{self.user}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew',null=True) #can not create two foreign keys referring to the same field in a foreign table, set related name for it
    status = models.BooleanField(db_index = True,default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    data = models.DateTimeField(db_index = True)
    def __str__(self):
        return f"{self.data}"
class OrderItem(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together = ('order', 'menuitem')
    def __str__(self):
        return f"{self.order}"