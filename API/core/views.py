from django.http import Http404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Comissions, Sellers, Month_Comissions
from .serializers import ComissionsSerializer, SellersSerializer, Month_ComissionsSerializer
import numpy as np

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
    def calculate_comission(self, id_seller, amount):
        try:
            seller = Sellers.objects.get(pk=id_seller)
            id_comission = seller.get_id_comission()
            plan_comission = Comissions.objects.get(pk=id_comission)

            if(amount >= plan_comission.get_min_value()):
                return amount * (plan_comission.get_upper_percentage() / 100)
            else:
                return amount * (plan_comission.get_lower_percentage() / 100)
        except Exception as error:
            return error

    def get(self, request, format=None):
        month_comissions = Month_Comissions.objects.all()
        serializer = Month_ComissionsSerializer(month_comissions, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        id_seller = request.data['id_seller']
        request.data['comission'] = self.calculate_comission(
                                        id_seller,
                                        request.data['amount']
                                    )
        serializer = Month_ComissionsSerializer(data=request.data)

        if serializer.is_valid():
            content = serializer.save()
            return Response(
                        {"id": content.id, "comission": content.comission},
                        status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMonthComissionsDetail(APIView):

    def get_object(self, pk):
        try:
            return Month_Comissions.objects.get(pk=pk)
        except Month_Comissions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        serializer = Month_ComissionsSerializer(month_comissions)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        serializer = Month_ComissionsSerializer(month_comissions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        month_comissions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSellersMonth(APIView):
    def get(self, request, month):
        print(month)
        sellers = (Month_Comissions
                        .objects
                        .filter(month=month)
                        .order_by('-comission'))
        sellers = [{'name': s.id_seller.name,
                     'id': s.id_seller.id,
                    'comission': s.comission} for s in sellers]
        return Response(sellers, status=status.HTTP_200_OK)

class EmailListComission(APIView):

    def get(self, request, format=None):
        month_comissions = Month_Comissions.objects.all()
        serializer = Month_ComissionsSerializer(month_comissions, many=True)
        
        return Response({"content": serializer.data})
            
    def post(self, request):
        seller = Sellers.objects.get(pk=request.data['id_seller'])
        sales = Month_Comissions.objects.filter(id_seller=seller.id)
        amount = [s.amount for s in sales]
        if len(amount)>=5:
            amount = np.array(sorted(amount[-5:]))
            weights = np.array([0,0,1,2,3])
            meta = (amount.dot(weights)/weights.sum())*.9
            if (request.data['amount']<= meta):
                subject = 'Notificação'
                msg = 'Vendedor não atingiu a meta'
                _from = "a@empresa.com"
                _to = [seller.email]

                send_mail(subject, msg, _from, _to,
                          fail_silently=False)

                res = {"should_notify": True}
                return Response(res,status=status.HTTP_200_OK)

            res = {"seller": seller.id, 
                   "amount": request.data['amount'],
                   "meta": meta}
            return Response(res,status=status.HTTP_200_OK)
        else:
            res = {"content": "Vendedor tem menos de 5 meses de vendas"}
            return Response(res, status=status.HTTP_200_OK)

