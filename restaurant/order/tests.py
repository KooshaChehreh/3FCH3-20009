from model_bakery import baker
from users.models import User
from test_utils import make_authenticated_api_client
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from exceptions import *
from rest_framework import status
from django.utils import timezone
from order.models import Table, Order
from unittest.mock import patch
from django.urls import reverse
from django.conf import settings


class TableViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = baker.make(User, username="parstasmim", password=make_password("pars123"))

        self.user_authenticated_client = make_authenticated_api_client(user=self.user)
        self.not_authenticated_client = APIClient()

    def test_create_table_success(self):
        data = {
            "name": "Table 2",
            "seats_number": 6,
        }
        url = reverse("tables-list")
        response = self.user_authenticated_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(Table.objects.get(name=data["name"]).table_state, Table.TABLE_AVAILABLE)
    
    def test_create_table_unauthorized(self):
        data = {
            "name": "Table 2",
            "seats_number": 6,
        }
        url = reverse("tables-list")
        response = self.not_authenticated_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    @patch('order.models.Table.check_table_numbers')  # Mock the check_table_numbers method
    def test_create_table_exceed_limit(self, mock_check_table_numbers):
        mock_check_table_numbers.return_value = False
        data = {
            "name": "Table 2",
            "seats_number": 6,
        }
        url = reverse("tables-list")
        response = self.user_authenticated_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], ExceededTableNumbers.default_code)

    def test_book_table_success(self):
        table = baker.make(Table, seats_number=10)
        data = {
            "number_of_guests": 1
        }
        url=reverse("tables-book", kwargs={"pk":table.id})
        response = self.user_authenticated_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Table.objects.get(id=table.id).table_state, Table.TABLE_RESERVED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.filter().first().order_price, (4-1) * settings.TABLE_SEAT_COST)

    # def test_book_table_not_available(self):
    #     self.table.table_state = Table.TABLE_RESERVED
    #     self.table.save()

    #     data = {
    #         "number_of_guests": 3
    #     }
    #     response = self.client.post(f'/api/tables/{self.table.id}/book/', data)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_book_table_exceed_capacity(self):
    #     data = {
    #         "number_of_guests": 5  # Exceeds the table's seats_number (4)
    #     }
    #     response = self.client.post(f'/api/tables/{self.table.id}/book/', data)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         response.data['message'],
    #         "Number of guests exceeds table capacity (4)."
    #     )

    # def test_book_table_no_guests_provided(self):
    #     data = {}  # Missing `number_of_guests`
    #     response = self.client.post(f'/api/tables/{self.table.id}/book/', data)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         response.data['message'],
    #         "Number of guests is required."
    #     )

    # def test_cancel_order_success(self):
    #     order = Order.objects.create(
    #         user_id=1,
    #         table_id=self.table.id,
    #         number_of_guests=3,
    #         order_price=100,
    #         order_state=Order.ORDER_ACTIVE
    #     )
    #     self.table.table_state = Table.TABLE_RESERVED
    #     self.table.save()

    #     data = {
    #         "order_id": order.id
    #     }
    #     response = self.client.post('/api/tables/cancel/', data)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(order.refresh_from_db().order_state, Order.ORDER_CANCELED)
    #     self.assertEqual(self.table.refresh_from_db().table_state, Table.TABLE_AVAILABLE)

    # def test_cancel_order_not_found(self):
    #     data = {
    #         "order_id": 999  # Non-existent order ID
    #     }
    #     response = self.client.post('/api/tables/cancel/', data)

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_cancel_table_not_found(self):
    #     order = Order.objects.create(
    #         user_id=1,
    #         table_id=999,  # Non-existent table ID
    #         number_of_guests=3,
    #         order_price=100,
    #         order_state=Order.ORDER_ACTIVE
    #     )

    #     data = {
    #         "order_id": order.id
    #     }
    #     response = self.client.post('/api/tables/cancel/', data)

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
