from django.urls import path, include
from .views import ListComissions, ListComissionDetail

urlpatterns = [
    path('listComissions/', ListComissions.as_view(), name='list_comissions'),
    path('listComissionsDetail/<int:pk>', ListComissionDetail.as_view(),
         name='list_comissions_detail')
]
