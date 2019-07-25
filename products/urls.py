from django.contrib import admin
from django.urls import path,re_path
from . import views
urlpatterns = [
    # path('', views.pro , name="prod"),
    # path('<int:id>',views.pro,name="prod"),
    path('',views.ProductListView.as_view(template_name="products/listview.html"),name="productlistview"),
    re_path(r'^(?P<id>\d+)/$',views.pro,name="prod"),
    path('cbv/<int:pk>',views.ProductDetailView.as_view(),name="prod-detailclass"),
]
