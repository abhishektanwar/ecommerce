from django.contrib import admin
from django.urls import path,re_path
from . import views
urlpatterns = [
    # path('', views.pro , name="prod"),
    # path('<int:id>',views.pro,name="prod"),
    path('', views.CategoryListView.as_view() , name="category-list"),
    re_path('(?P<slug>[\w-]+)/', views.CategoryDetailView.as_view() , name="category-detail"),
    # path('',views.ProductListView.as_view(template_name="products/listview.html"),name="productlistview"),
    # re_path(r'^(?P<id>\d+)/$',views.pro,name="prod"),
    # path('cbv/<int:pk>',views.ProductDetailView.as_view(),name="prod-detailclass"),
    # path('cbv/<int:pk>/inventory',views.VariationListView.as_view(),name="variation-listclass"),
    # path('<int:pk>/listvariations/',views.VariationEditList ,name="inventory-edit-list"),
    # path('<int:pk>/editvariations/',views.VariationEditView ,name="edit-variation"),
]
