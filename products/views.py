from django.shortcuts import render,get_object_or_404 , redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from .models import Product,Variation,Category
from .forms import VariationInventoryForm
# Create your views here.


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        instance = self.get_object()
        # instance here is the product selected by used to see detail of
        # print(instance)
        context["related"] = Product.objects.get_relatedproducts(instance).order_by("?")[:4]
        # print(context["related"][0].productimage_set.first().image.url)
        # for item in context["related"]:
        #     img = item.productimage_set.first()
        #     if img:
        #         print(img.image.url)
        #     else:
        #         print("none")  
          
        return context
class ProductListView(ListView):
    model=Product
    queryset = Product.objects.ru()
    context_object_name = 'dhj'
    # by defalut context is passed in a variable named object_list , variable name can
    # be overwritten by passing context_object_name

    
    # to show active products only we can do this  or use product manager(models.py)
    # queryset=Product.objects.all().filter(active=True)
    # get_context_data is used to pass additional context apart from model to view(template)
    def get_context_data(self,*args, **kwargs):
        
        context = super(ProductListView,self).get_context_data(*args ,**kwargs)
        # context["some_other_arguments_forhtmlpage"] = argumnet
        context["now"] = timezone.now()
        return context
    # queryset bydefault is model_name.objects.all() but to pass filtered data to template as context
    # get_queryset is used(overwritten) 
    #function responsible for searching of product
    def get_queryset(self,*args,**kwargs):
        qs = super(ProductListView, self).get_queryset(*args,**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains = query)
            )
            try:
                qs_price = self.model.objects.filter(Q(price=query))
                qs = (qs | qs_price).destinct()
            except:
                pass
        return qs    


class VariationListView(ListView):
    model=Variation
    queryset = Variation.objects.all()
    context_object_name = 'dhj'
    # by defalut context is passed in a variable named object_list , variable name can
    # be overwritten by passing context_object_name

    
    # to show active products only we can do this  or use product manager(models.py)
    # queryset=Product.objects.all().filter(active=True)
    # get_context_data is used to pass additional context apart from model to view(template)
    def get_context_data(self,*args, **kwargs):
        
        context = super(VariationListView,self).get_context_data(*args ,**kwargs)
        # context["some_other_arguments_forhtmlpage"] = argumnet
        context["now"] = timezone.now()
        context["product_key"] = self.kwargs['pk']
        return context
    # queryset bydefault is model_name.objects.all() but to pass filtered data to template as context
    # get_queryset is used(overwritten) 
    #function responsible for searching of product
    #getting product object related to pk passed, if present
    # variations for that product are fetched
    def get_queryset(self,*args,**kwargs):
        qs= super(VariationListView, self).get_queryset(*args,**kwargs)
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product,pk=product_pk)
            qs = Variation.objects.filter(product=product)
        return qs    

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

def VariationEditList(request,pk):
    product = get_object_or_404(Product,pk=pk)
    qs=Variation.objects.filter(product=product)
    print(qs.count())
    for item in qs:
        
        form = VariationInventoryForm()
    context={"product_pk":pk,"form":form,"qs":qs}
    return render(request,'products/variation_edit.html',context)

def VariationEditView(request,pk):
    item = Variation.objects.get(pk=pk)
    if request.method == 'POST' :
        print(request.POST)
        form = VariationInventoryForm(data=request.POST)
        if form.is_valid():
            print(request.POST.get("price"))
            form.save(commit=False)
            form.save()
            return redirect('/product')
        
    else:
        data = {'price':item.price , 'sale_price':item.sale_price , 'inventory':item.inventory}
        form = VariationInventoryForm(initial=data)
    context = {"form":form}
    return render(request,"products/edit_inventory.html",context)

class CategoryListView(ListView):
    model = Category
    query_set = Category.objects.all()
    template_name = "products/categorylist.html"
class CategoryDetailView(DetailView):
    model = Category
    template_name = "products/categorydetail.html"
    
    def get_context_data(self,*args,**kwargs):
        context = super(CategoryDetailView,self).get_context_data(*args,**kwargs)
        obj = self.get_object()
        products_set = obj.product_set.all()
        default_products = obj.default_category.all() 
        products =(products_set | default_products).distinct()
        context["products"] = products
        print(products)
        return context