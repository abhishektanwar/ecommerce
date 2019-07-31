from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
# Create your models here.

# if a product is in inactive ,we dont want to show it in the product list
#model manager is often used to make custom query sets
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):  
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def ru(self,*args,**kwargs):
        return self.get_queryset().active()

    def get_relatedproducts(self,instance):
        # instance is the product selected by user
        # product_one is the list of products whose category is same as selected by user
        # product_two is the list of products whose default is same as selected by user
        products_one = self.get_queryset().filter(categories__in=instance.categories.all())
        product_two = self.get_queryset().filter(default = instance.default)
        qs = (products_one | product_two).exclude(id=instance.id).distinct()

        return qs


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank = True,null = True)
    active = models.BooleanField(default = True)
    price = models.DecimalField(decimal_places = 2,max_digits=6)
    # invenstory?
    # slug
    categories = models.ManyToManyField('Category',blank=True)
    default = models.ForeignKey('Category',related_name='default_category',null=True,blank=True,on_delete=models.CASCADE)

    objects = ProductManager()
    
    def __str__(self):
        return self.title

    # productdetailview in views.py returns products whose type is Product(model)
    # that is why it get_image_url is defined here because only Product type can call this function
    def get_image_url(self):
        print(self)
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img    

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


#creating a default variation when a new product is created
def product_post_saved_receiver(sender,instance,created,**kwargs):
    # print(instance)
    product = instance
    variation = product.variation_set.all()
    if variation.count() == 0:
        new_variation = Variation()
        new_variation.product = product
        new_variation.title = "Default"
        new_variation.price = product.price
        new_variation.save()
post_save.connect(product_post_saved_receiver,sender=Product)


def image_upload_to(instance, filename):
#instance is the title of product to which image being uploaded is linked to
    # print(instance)
    title = instance.product.title
    slug = slugify(title)
    # the name of the file(img) being uploaded can also be changed
    basename , extension = filename.split(".")
    new_filename = "%s-%s.%s"%(slug,instance.id,extension)#instance.id is id of product being referred to
    return "products/%s/%s" %(slug,filename)

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title

class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True,blank = True)
    active= models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.title

