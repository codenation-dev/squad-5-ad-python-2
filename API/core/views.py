from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comissions, Sellers, Month_Comissions
from .serializers import ComissionsSerializer, SellersSerializer, Month_ComissionsSerializer
from rest_framework import status
from django.http import Http404


class ListComissions(APIView):

    def get(self, request, format=None):
        comissions = Comissions.objects.all()
        serializer = ComissionsSerializer(comissions, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        serializer = ComissionsSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListComissionDetail(APIView):

    def get_object(self, pk):
        try:
            return Comissions.objects.get(pk=pk)
        except Comissions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comission = self.get_object(pk)
        comission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSellers(APIView):

    def get(self, request, format=None):
        sellers = Sellers.objects.all()
        serializer = SellersSerializer(sellers, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        serializer = SellersSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSellersDetail(APIView):

    def get_object(self, pk):
        try:
            return Sellers.objects.get(pk=pk)
        except Sellers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        seller = self.get_object(pk)
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListMonthComissions(APIView):

    def get(self, request, format=None):
        month_comissions = Month_Comissions.objects.all()
        serializer = Month_ComissionsSerializer(month_comissions, many=True)
        return Response({"content": serializer.data})

    def post(self, request):        
        id_seller = request.data['id_seller']
        request.data['comission'] = calculate_comission(id_seller, request.data['amount'])
        serializer = Month_ComissionsSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id, "comission": content.comission}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_comission(id_seller, amount):
    seller = Sellers.objects.get(pk=id_seller)
    id_comission = seller.get_id_comission()
    plan_comission = Comissions.objects.get(pk=id_comission)

    if(amount >= plan_comission.get_min_value()):
        return amount * (plan_comission.get_upper_percentage() / 100)
    else:
        return amount * (plan_comission.get_lower_percentage() / 100)
    