from django.db import models
from django.contrib.auth.models import User,Group



class MenuItem(models.Model):
    title=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.SmallIntegerField()
    

    def __str__(self):
     return self.title
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    
    
    quantity = models.SmallIntegerField()
    
    
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
       
        unique_together = ('menuitem', 'user')



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True, auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')


