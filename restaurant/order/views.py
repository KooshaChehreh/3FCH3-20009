from django.shortcuts import render
from rest_framework import viewsets, filters, status
from order.models import Table, Order
from order.serializer import TableSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import action   
from exceptions import *



class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def create(self, request, *args, **kwargs):
        if Table.check_table_numbers():
            return super().create(request, *args, **kwargs)
        return Response(
            data={"message": "تعداد میزها بیشتر از حد مجاز است"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    @action(detail=True, methods=['post'])

    # booking serializer should be added
    def book(self, request, pk=None):
        try:
            table = self.get_object()
            number_of_guests = request.data.get('number_of_guests')
            user_id = request.user.id
            table_id = request.data.get('table_id')
            try:
                table = Table.objects.get(id=table_id)
            except Table.DoesNotExist:
                raise TableDoesNotExist
            
            
            if table._state == Table.TABLE_RESERVED:
                raise TableReserved
            
            if number_of_guests is None:
                return Response(
                    {"message": "Number of guests is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            number_of_guests = int(number_of_guests)
            if number_of_guests > table.seats_number:
                return Response(
                    {"message": f"Number of guests exceeds table capacity ({table.seats_number})."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order = Order.objects.create(
                user_id=user_id,
                table_id=table_id,
                number_of_guests=Order.adjust_odd_guests(number_of_guests),
                order_price=Order.caclulate_order_price(number_of_guests),
            )
            
            return Response(data=OrderSerializer(order).data, status=status.HTTP_200_OK)

        except Table.DoesNotExist:
            return Response(
                {"message": "The specified table does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            ) 