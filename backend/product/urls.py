from django.urls import path

from .views import GetListProductApiView, ProductMixinsViews

# from .views import ListProductApiView, CreateProductApiView, DeleteProductApiView, DetailProductApiView, GetListProductApiView, ProductMixinsViews, UpdateProductApiView, api_view 

urlpatterns = [
    # path('',api_view,name='api_view'),
    # path('<int:pk>/', DetailProductApiView.as_view()),
    # path('create/',CreateProductApiView.as_view()),
    # path('update/<int:pk>/',UpdateProductApiView.as_view()),
    # path('delete/<int:pk>/',DeleteProductApiView.as_view()),
    path('get_create_list/',GetListProductApiView.as_view()),
    # path('list_create/',ListProductApiView.as_view()),
    path('create/',ProductMixinsViews.as_view()),
    path('detail/<int:pk>/',ProductMixinsViews.as_view(),name="product-detail"),
    path('update/<int:pk>/',ProductMixinsViews.as_view()),
    path('delete/<int:pk>/',ProductMixinsViews.as_view()),
    path('list/',ProductMixinsViews.as_view()),


]
