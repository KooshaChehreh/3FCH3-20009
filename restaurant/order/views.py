from django.shortcuts import render
from rest_framework import viewsets, filters, status
from order.models import Table, Order
from order.serializer import TableSerializer, OrderSerializer, BookSerializer, CancelSerializer
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
    def book(self, request, pk=None):
        table = self.get_object()
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        number_of_guests = serializer.validated_data.get("number_of_guests")
        user_id = request.user.id
            
        if table.table_state != Table.TABLE_AVAILABLE:
            raise TableNotReservable
        
        if number_of_guests is None:
            return Response(
                {"message": "Number of guests is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        table.table_state = Table.TABLE_RESERVED
        table.save()
        
        return Response(data=OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def cancel(self, request, pk=None):
        """
            I have considered that both user and admin can use the api. If not, a permission should be implemented
        """
        serializer = CancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order_id")
        try:
            order = Order.objects.get(id=order_id)
            table = Table.objects.get(id=order.table_id)
        except Order.DoesNotExist:
            raise OrderNotFound
        except Table.DoesNotExist:
            raise TableDoesNotExist
        order.order_state = Order.ORDER_CANCELED
        table.table_state = Table.TABLE_AVAILABLE
        order.save()
        table.save()
        return Response(status=status.HTTP_200_OK)
