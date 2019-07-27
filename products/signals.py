# from django.db.models.signals import post_save
# from .models import Product,Variation

# from django.dispatch import receiver

# @receiver(post_save,sender=Product)
# def create_variation(sender,instance,created,*args,**kwargs):
#     if created:
#         Variation.objects.create(product=instance)


# @receiver(post_save,sender=Product)
# def save_variation(sender,instance,created,*args,**kwargs):
#     product = instance
#     variation = product.variation_set.all()
#     if variation.count() == 0:
#         new_variation = Variation()
#         new_variation.product = product
#         new_variation.title = "Default"
#         new_variation.price = product.price
#         instance.new_variation.save()