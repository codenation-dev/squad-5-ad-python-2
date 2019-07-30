from django.test.client import Client
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from core.models import Sellers, Comissions, Month_Comissions
from datetime import datetime, time
from decimal import Decimal
import numpy as np


class EndPointTests(APITestCase):
    # /comissions/
    def post(self, url, data, model=None):
        response = self.client.post(url, data, type="json")
        if model is None:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['id'], model.objects.last().id)

    def get_all(self, url, model):
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['content']),
                         model.objects.count())

    def get_id(self, url):
        pk_id = np.random.randint(1, 10)
        url = url+str(pk_id)
        response = self.client.get(url, format='json')
        if response.status_code == status.HTTP_404_NOT_FOUND:
                error = ErrorDetail("Não encontrado.", code="not_found")
                self.assertEqual(response.data['detail'], error)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['id'], pk_id)

    def delete(self, url):
        pk_id = np.random.randint(1, 10)
        pk_id = 4
        url = url+str(pk_id)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['id'], pk_id)

    def put(self, url, data):
        response = self.client.put(url, data, type="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], pk_id)

    def test_post_comissions(self):
        url = "/comissions/"
        data = {
            "lower_percentage": 2.0,
            "min_value": 800.0,
            "upper_percentage": 6.0
            }

        self.post(url, data, Comissions)

    def test_get_all_comissions(self):
        self.get_all("/comissions/", Comissions)

    # /comissions/<id>
    def test_get_id_comissions(self):
        self.get_id("/comissions/")

    def test_put_comissions(self):
        pk_id = np.random.randint(1, 10)
        pk_id = 2
        url = "/comissions/"+str(pk_id)
        data = {
            "lower_percentage": 2.0,
            "min_value": 300,
            "upper_percentage": 6.0
            }
        self.put(url, data)

    def test_delete_comissions(self):
        self.delete("/comissions/")

    # /sellers/
    def test_post_sellers(self):
        url = "/sellers/"
        data = {
            "name": "Ines",
            "address": "Rua do italo",
            "phone": "123654789",
            "age": 15,
            "email": "email@email.com",
            "cpf": "12345612312",
            "comission": 2
        }
        self.post(url, data, Sellers)

    def test_get_all_sellers(self):
        self.get_all("/sellers/", Sellers)

    # /sellers/<id>
    def test_get_id_sellers(self):
        self.get_id("/sellers/")

    def test_put_sellers(self):
        pk_id = np.random.randint(1, 10)
        url = "/sellers/"+str(pk_id)
        data = {
            "name": "Ines",
            "address": "Rua do italo",
            "phone": "123654789",
            "age": 15,
            "email": "email@email.com",
            "cpf": "12345612312",
            "comission": 2
        }
        self.put(url, data)

    def test_delete_sellers(self):
        self.delete("/sellers/")

    # /month_sales/
    # def test_post_month_sales(self):
        url = "/month_sales/"
        data = {
            "id_seller": 1,
            "amount": 10000.0,
            "month": 2
        }
        self.post(url, data, Month_Comissions)

    def test_get_all_month_sales(self):
        self.get_all("/month_sales/", Month_Comissions)

    # /month_sales/
    def test_get_id_month_sales(self):
        self.get_id("/month_sales/")

    # def test_put_month_sales(self):

    def test_delete_month_sales(self):
        self.delete("/month_sales/")

    # /vendedores/<id>
    def test_get_id_vendedores(self):
        pk_id = np.random.randint(1, 12)
        self.get_all(f"/vendedores/{pk_id}", Month_Comissions)

    # /check_comission/
    def test_post_check_comission(self):
        url = "/check_comission/"
        data = {
            "seller": 2,
            "amount": 1000.65
        }
        self.post(url, data)
