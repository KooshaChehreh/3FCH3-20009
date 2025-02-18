from celery import shared_task
from order.models import Order

@shared_task
def create_order():
    Order.objects.create(user_id=1, table_id=1, number_of_seat=2, order_price=1000)
    return "object added."