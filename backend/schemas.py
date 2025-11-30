from typing import List, Optional
from pydantic import BaseModel

# Схемы для марки
class BrandCreate(BaseModel):
    name: str

class BrandResponse(BaseModel):
    id: int
    name: str

# Схемы для модели
class ModelCreate(BaseModel):
    name: str

class ModelResponse(BaseModel):
    id: int
    name: str

# Схемы для паркинга
class ParkingCreate(BaseModel):
    name: str

class ParkingResponse(BaseModel):
    id: int
    name: str

# Схемы для сотрудника
class EmployeeCreate(BaseModel):
    full_name: str

class EmployeeResponse(BaseModel):
    id: int
    full_name: str

# Схемы для платежа
class PaymentCreate(BaseModel):
    contract_id: int
    date: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    contract_id: int
    date: str
    amount: float

# Схемы для клиента
class ClientResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    license_number: str
    birth_date: Optional[str] = None

class ClientCreate(BaseModel):
    full_name: str
    phone: str
    license_number: str
    birth_date: str

# Схемы для автомобиля
class CarResponse(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    color: str
    license_plate: str
    price: float

class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    color: str
    plate: str
    price: float

class CarUpdate(BaseModel):
    color: str
    plate: str
    price: float

# Схемы для договора
class ContractResponse(BaseModel):
    id: int
    client: ClientResponse
    car: CarResponse
    start_date: str
    end_date: str
    payment_date: str
    amount: Optional[float] = None
    status: str

class ContractCreate(BaseModel):
    client_id: int
    car_id: int
    start_date: str
    end_date: str
    payment_date: str
    amount: float

# Схемы для страховки
class InsuranceCreate(BaseModel):
    contract_id: int
    cost: float

class InsuranceResponse(BaseModel):
    id: int
    contract: ContractResponse
    cost: float

# Схемы для обслуживания
class MaintenanceCreate(BaseModel):
    car_id: int
    description: str
    date: str
    cost: float

class MaintenanceResponse(BaseModel):
    id: int
    car: CarResponse
    description: str
    date: str
    cost: float
