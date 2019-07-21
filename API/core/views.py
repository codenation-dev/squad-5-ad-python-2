from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comissions, Sellers, Month_Comissions
from .serializers import ComissionsSerializer, SellersSerializer, Month_ComissionsSerializer
from rest_framework import status
from django.http import Http404

import json


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
        id_seller = request.data['id_seller']
        request.data['amount'] = check_comission(
                                        id_seller,
                                        request.data['month']
                                    )
        serializer = Month_ComissionsSerializer(data=request.data)

        if serializer.is_valid():
            content = serializer.save()
            return Response(
                    {"id": content.id, "amount": content.amount},
                    status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_comission(self, request):
        
        all_months_amount = [request.data(Month_Comissions.amount)]
        n = len(all_months_amount)
        all_months = sum(all_months_amount)
       
        media_all_months = all_months / n             
        percent = all_months * 10 / 100
        if all_months < media_all_months - percent: 
            self.send_mail()
        else:
            pass

        def send_mail(self, request, subject, message, from_email):
            subject = request.POST.get('subject', '') #email dos vendedores com pouscas vendas
            message = request.POST.get('message', '') #escrever msg geral aos vendedores
            from_email = request.POST.get('from_email', '') #email adm

            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ['admin@example.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/contact/thanks/')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')




