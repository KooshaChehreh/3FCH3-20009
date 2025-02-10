from django.db import models
from utils import seats_number_validator
from django.conf import settings

class Table(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="نام میز",
    )
    seats_number = models.IntegerField(
        validators=[seats_number_validator],
        verbose_name="تعداد صندلی",
    )

    TABLE_RESERVED = "R"  
    TABLE_AVAILABLE = "A" 
    TABLE_STATE_CHOICES = [
        (TABLE_RESERVED, "رزرو شده"),
        (TABLE_AVAILABLE, "در دسترس"),
    ]
    table_state = models.CharField(
        max_length=1,
        choices=TABLE_STATE_CHOICES,
        default=TABLE_AVAILABLE,
        verbose_name="وضعیت میز",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="ایجاد شده در"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="بروز شده در")


    class Meta:
        verbose_name = "میز"
        verbose_name_plural = "میزها"
        ordering = ["-id"]

    @staticmethod
    def check_table_numbers() -> bool:
        if Table.objects.count() > 10:
                return False
        return True
    

class Order(models.Model):
    user_id = models.IntegerField(
        verbose_name="شناسه کاربر",
    )
    table_id = models.IntegerField(
         verbose_name="شناسه میز",
    )
    number_of_seat = models.IntegerField(
        validators=[seats_number_validator],
        verbose_name="تعداد نفرات",
    )
    order_price = models.IntegerField(
         verbose_name="قیمت سفارش"
         )

    ORDER_DONE = "D" 
    ORDER_SUBMITTED = "S"  
    ORDER_CANCELED = "C" 

    ORDER_STATE_CHOICES = [
        (ORDER_DONE, "سفارش انجام شده"),
        (ORDER_SUBMITTED, "سفارش ثبت شده"),
        (ORDER_CANCELED, "سفارش لغو شده"),

    ]
    order_state = models.CharField(
        max_length=1,
        choices=ORDER_STATE_CHOICES,
        default=ORDER_SUBMITTED,
        verbose_name="وضعیت سفارش",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="ایجاد شده در"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="بروز شده در")


    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ["-id"]
    
    @staticmethod
    def caclulate_order_price(number_of_seat):
        return (number_of_seat - 1) * settings.TABLE_SEAT_COST
    
    @staticmethod
    def adjust_odd_guests(number_of_seat):
        if number_of_seat < 4:
            number_of_seat = 4
            return number_of_seat
        
        if number_of_seat % 2 != 0:
            return number_of_seat + 1
        else:
            return number_of_seat