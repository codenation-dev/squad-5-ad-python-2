from django.urls import path, include
from .views import ListComissions, ListComissionDetail, ListSellers, ListSellersDetail

urlpatterns = [
    path('listComissions/', ListComissions.as_view(), name='list_comissions'),
    path('listComissionsDetail/<int:pk>', ListComissionDetail.as_view(),
         name='list_comissions_detail'),
    path('listSellers/', ListSellers.as_view(), name='list_sellers'),
    path('listSellersDetail/<int:pk>', ListSellersDetail.as_view(),
         name='list_sellers_detail'),
]
