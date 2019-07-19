from django.urls import path, include
from .views import (ListComissions, 
                    ListComissionDetail, 
                    ListSellers, 
                    ListSellersDetail, 
                    ListMonthComissions,
                    ListMonthComissionsDetail)

urlpatterns = [
    #  GET all, POST
     path('comissions/', ListComissions.as_view(), name='list_comissions'),
    #  PUT , DELETE
     path('comissions/<int:pk>', ListComissionDetail.as_view(),
         name='list_comissions_detail'),
    #  GET all, POST
     path('sellers/', ListSellers.as_view(), name='list_sellers'),
    #  PUT , DELETE

     path('sellers/<int:pk>', ListSellersDetail.as_view(),
         name='list_sellers_detail'),
    #  GET all, POST
     path('month_comissions/', ListMonthComissions.as_view(), name='month_comissions'),
     path('month_comissions/<int:pk>', ListMonthComissionsDetail.as_view(), name='month_comissions_detail'),
]
