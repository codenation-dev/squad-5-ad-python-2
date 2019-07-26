from django.urls import path, include
from django.conf.urls import url
from .views import (ViewComissions,
                    ViewComissionDetail,
                    ViewSellers,
                    ViewSellersDetail,
                    ViewMonthComissions,
                    ViewMonthComissionsDetail,
                    ViewSellersMonth,
                    ViewEmailComission)
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Gestão de comissões Televendas')


urlpatterns = [
    url("", schema_view),
    #  GET all, POST
    path('comissions/',
         ViewComissions.as_view(),
         name='list_comissions'),
    #  PUT , DELETE
    path('comissions/<int:pk>',
         ViewComissionDetail.as_view(),
         name='list_comissions_detail'),
    #  GET all, POST
    path('sellers/',
         ViewSellers.as_view(),
         name='list_sellers'),
    #  PUT , DELETE
    path('sellers/<int:pk>',
         ViewSellersDetail.as_view(),
         name='list_sellers_detail'),
    #  GET all, POST
    path('month_sales/',
         ViewMonthComissions.as_view(),
         name='month_comissions'),
    #  PUT , DELETE
    path('month_sales/<int:pk>',
         ViewMonthComissionsDetail.as_view(),
         name='month_comissions_detail'),
    #  GET
    path('vendedores/<int:month>',
         ViewSellersMonth.as_view(),
         name='month_comissions_detail'),
    #  POST
    path('check_comission/',
         ViewEmailComission.as_view(),
         name='email_comissions')]
