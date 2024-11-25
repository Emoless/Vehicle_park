from pydantic import BaseModel, Field
from typing import Optional


class Driver(BaseModel):
    name: str
    experience: int
    phone: int
    email: str
    status: str = Field(default="available")  # Дефолтное значение


class Vehicle(BaseModel):
    brand: str
    reg_num: str  # Тип изменен на str, так как регистрационный номер обычно строка
    mileage: int
    status: str = Field(default="available")  # Дефолтное значение


class Task(BaseModel):
    route: str
    driver_id: int  # Обязательная внешняя ссылка
    status: str = Field(default="pending")  # Дефолтное значение
    car_id: int  # Обязательная внешняя ссылка
