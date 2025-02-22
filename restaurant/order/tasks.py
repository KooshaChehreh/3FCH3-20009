from celery import shared_task
from order.models import Order
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.db import IntegrityError
from datetime import timedelta
from restaurant.celery import app
import logging

logger = logging.getLogger(__name__)

@app.task(name="create_order_task")  
def create_order():
    try:
        Order.objects.create(user_id=1, table_id=1, number_of_seat=2, order_price=1000)
        logger.info("Order created successfully")
        return "Order created successfully"
    except IntegrityError as e:
        logger.error(f"Error creating order: {e}")
        return f"Error: {e}"

@app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(timedelta(seconds=10), create_order.s(), name="Create Order Task")
    # schedule, created = CrontabSchedule.objects.get_or_create(
    #     minute="*/1", hour="*", day_of_week="*", day_of_month="*", month_of_year="*"
    # )

    # PeriodicTask.objects.get_or_create(
    #     crontab=schedule,
    #     name="Sample Task",
    #     task="create_order_task" 
    # )
    # print("Periodic task added")
    # return "Periodic task added."