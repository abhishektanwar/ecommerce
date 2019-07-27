from django.shortcuts import render,get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404
from django.utils import timezone

from .models import Product
# Create your views here.


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    
class ProductListView(ListView):
    model=Product
    queryset = Product.objects.ru()
    

    
    # to show active products only we can do this  or use product manager(models.py)
    # queryset=Product.objects.all().filter(active=True)
    def get_context_data(self,*args, **kwargs):
        
        context = super(ProductListView,self).get_context_data(*args ,**kwargs)
        # context["some_other_arguments_forhtmlpage"] = argumnet
        # context["now"] = timezone.now()
        return context

def pro(request,id):
    # instance = get_object_or_404(Product,id=id)
    try:
        instance = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    except:
        raise Http404
    context ={
        "object":instance
    }
    return render(request,"products/detail.html",context)