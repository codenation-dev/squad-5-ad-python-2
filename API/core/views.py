from django.http import Http404, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from .models import Comissions, Sellers, Month_Comissions
from .serializers import (ComissionsSerializer,
                          SellersSerializer,
                          Month_ComissionsSerializer)


import numpy as np


def index(request):

    data = {
        "title": "API Gestão de comissões Televendas",
        "resources": [
            {"path": "comissions/", "methods": ["get", "post"]},
            {"path": "comissions/<id>", "methods": ["get", "put", "delete"]},
            {"path": "sellers/", "methods": ["get", "post"]},
            {"path": "sellers/<id>", "methods": ["get", "put", "delete"]},
            {"path": "month_sales/", "methods": ["get", "post"]},
            {"path": "month_sales/<id>", "methods": ["get", "put", "delete"]},
            {"path": "vendedores/<month>", "methods": "get"},
            {"path": "check_comission/", "methods": "post"}
        ]
    }

    return JsonResponse(data)


class ViewComissions(APIView):

    def get(self, request, format=None):
        """
            Retorna todos os planos de comissão existentes
        """
        comissions = Comissions.objects.all()
        serializer = ComissionsSerializer(comissions, many=True)
        return Response({"content": serializer.data})

    def post(self, request):
        """
        post:
            Cria um novo plano de comissão

        """

        serializer = ComissionsSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response({"id": content.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewComissionDetail(APIView):
    """
    get:
        Retorna todos os planos de comissão existentes

    put:
        Atualiza um plano de comissão existente

    delete:
        Deleta um plano de comissão existente

    """

    def get_object(self, pk):
        try:
            return Comissions.objects.get(pk=pk)
        except Comissions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        comission = self.get_object(pk)
        serializer = ComissionsSerializer(comission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comission = self.get_object(pk)
        comission.delete()
        return Response({"id": pk}, status=status.HTTP_204_NO_CONTENT)


class ViewSellers(APIView):
    """
    get:
        Retorna todos os vendedores existentes

    post:
        Cadastra um novo vendedor

    """
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


class ViewSellersDetail(APIView):
    """
    get:
        Retorna dados de um vendedor

    put:
        Atualiza dados do vendedor

    delete:
        Deleta um vendedor
    """
    def get_object(self, pk):
        try:
            return Sellers.objects.get(pk=pk)
        except Sellers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = SellersSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        seller = self.get_object(pk)
        seller.delete()
        return Response({"id": pk}, status=status.HTTP_204_NO_CONTENT)


class ViewMonthComissions(APIView):
    """
    get:
        Retorna todas a vendas realizadas

    post:
        Cadastra uma venda

    """
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
                        status=status.HTTP_201_CREATED
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewMonthComissionsDetail(APIView):
    """
    get:
        Retorna todas as vendas realizadas

    put:
        Atualiza um plano de comissão existente

    delete:
        Deleta um plano de comissão existente

    """
    def get_object(self, pk):
        try:
            return Month_Comissions.objects.get(pk=pk)
        except Month_Comissions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        serializer = Month_ComissionsSerializer(month_comissions)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        serializer = Month_ComissionsSerializer(month_comissions,
                                                data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        month_comissions = self.get_object(pk)
        month_comissions.delete()
        return Response({"id": pk}, status=status.HTTP_204_NO_CONTENT)


class ViewSellersMonth(APIView):
    """
    get:
        Retorna as vendas realizadas no mês indicado
    """
    def get(self, request, month):
        sellers = (Month_Comissions
                   .objects
                   .filter(month=month)
                   .order_by('-comission'))
        sellers = [{'name': s.id_seller.name,
                    'id': s.id_seller.id,
                    'comission': s.comission} for s in sellers]
        return Response({"content": sellers}, status=status.HTTP_200_OK)


class ViewEmailComission(APIView):
    """
    post:
        Verifica a média ponderada mensal do vendedor e o notifica
    """

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

    def check_comission(self, list_comissions, comission):
        list_comissions = np.array(list_comissions)
        weights = np.arange(1, list_comissions.shape[0]+1)
        mean = list_comissions.dot(weights)/weights.sum()
        if comission < (mean * 0.9):
            return True
        else:
            return False

    def send_mail(self, subject, message, from_email, to_email):
        if subject and message and from_email and to_email:
            try:
                send_mail(subject, message,
                          from_email, to_email,
                          fail_silently=False)
            except Exception as error:
                return error
            return "email enviado"
        else:
            return "Make sure all fields are entered and valid."

    def post(self, request):
        seller = Sellers.objects.get(pk=request.data['seller'])
        amount = request.data['amount']
        comission = self.calculate_comission(seller.pk, amount)

        sells = (Month_Comissions
                 .objects
                 .filter(id_seller=seller.pk)
                 .order_by('month'))
        sells = sorted([i['comission'] for i in sells.values()][-5:])

        should_notify = self.check_comission(sells, comission)

        if should_notify:
            subject = 'notificação televendas'
            message = 'comissão está abaixo da média'
            from_email = settings.EMAIL_HOST_USER
            to_email = [seller.email]
            result = self.send_mail(subject, message, from_email, to_email)
            print(result)
        return Response({"should_notify": should_notify},
                        status=status.HTTP_200_OK)
