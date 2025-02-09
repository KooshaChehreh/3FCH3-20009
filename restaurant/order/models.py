from django.db import models
from utils import seats_number_validator


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

    TABLE_RESERVED = "R"  # غیر همکار
    TABLE_AVAILABLE = "A"  # در حال ثبت نام و احرازهویت

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

    