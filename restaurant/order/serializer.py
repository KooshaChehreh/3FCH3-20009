from rest_framework import serializers
from order.models import Table, Order


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = [
            "id",
            "name",
            "seats_number",
            "table_state",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "table_id",
            "number_of_seat",
            "order_price",
            "order_state",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class BookSerializer(serializers.Serializer):
    number_of_guests = serializers.IntegerField()

class CancelSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()