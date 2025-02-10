from rest_framework.exceptions import APIException



class AccountSuspended(APIException):
    status_code = 400
    default_code = "account_suspended"
    default_detail = {
        "code": default_code,
        "message": "حساب کاربری تعلیق شده است و امکان ورود وجود ندارد.",
    }

class InvalidUsernameOrPassword(APIException):
    status_code = 400
    default_code = "invalid_username_or_password"
    default_detail = {
        "code": default_code,
        "message": "کلمه عبور یا کاربری وارد شده اشتباه است.",
    }

class UsernameAlreadyExists(APIException):
    status_code = 400
    default_code = "username_already_exists"
    default_detail = {
        "code": default_code,
        "message": "این نام کاربری تکراریست.",
    }


class SuspendedUser(APIException):
    status_code = 400
    default_code = "user_is_suspended"
    default_detail = {
        "code": default_code,
        "message": "کاربر بن شده است.",
    }

class UserDoesNotExist(APIException):
    status_code = 400
    default_code = "user_does_not_exist"
    default_detail = {
        "code": default_code,
        "message": "کاربر وجود ندارد.",
    }

class TableDoesNotExist(APIException):
    status_code = 400
    default_code = "table_does_not_exist"
    default_detail = {
        "code": default_code,
        "message": "میز مورد نظر وجود ندارد.",
    }

class TableNotReservable(APIException):
    status_code = 400
    default_code = "table_not_reservable"
    default_detail = {
        "code": default_code,
        "message": "این میز قابل رزرو شدن نیست.",
    }

class OrderNotFound(APIException):
    status_code = 400
    default_code = "table_not_reservable"
    default_detail = {
        "code": default_code,
        "message": "سفارش یافت نشد.",
    }

class ExceededTableNumbers(APIException):
    status_code = 400
    default_code = "number_of_tables_exceeded"
    default_detail = {
        "code": default_code,
        "message": "تعداد میز بیش از حد مجاز است.",
    }

class TableReachedCapacity(APIException):
    status_code = 400
    default_code = "table_reached_capacity"
    default_detail = {
        "code": default_code,
        "message": "تعداد نفرات از تعداد صندلی های میز بیشتر است.",
    }