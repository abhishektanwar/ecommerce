from django.db import models

# Create your models here.

# if a product is in inactive ,we dont want to show it in the product list

class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):  
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def ru(self,*args,**kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank = True,null = True)
    active = models.BooleanField(default = True)
    price = models.DecimalField(decimal_places = 2,max_digits=6)
    # invenstory?
    # slug
    objects = ProductManager()
    
    def __str__(self):
        return self.title
#PRODUCT VARIATION(SIZES ETC)
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    sale_price = models.DecimalField(max_digits=20,decimal_places=2 , null=True , blank = True)#initiall sale_price in not defined
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True,blank=True)  #refers none==unlimited amount
     
    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

        