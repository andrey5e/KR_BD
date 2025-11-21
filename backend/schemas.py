from pydantic import BaseModel
from typing import List, Optional

# Brand
class BrandCreate(BaseModel):
    name: str

class BrandResponse(BaseModel):
    id: int
    name: str

# Model
class ModelCreate(BaseModel):
    name: str

class ModelResponse(BaseModel):
    id: int
    name: str

# Parking
class ParkingCreate(BaseModel):
    name: str

class ParkingResponse(BaseModel):
    id: int
    name: str

# Employee
class EmployeeCreate(BaseModel):
    full_name: str

class EmployeeResponse(BaseModel):
    id: int
    full_name: str

# Payment
class PaymentCreate(BaseModel):
    contract_id: int
    date: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    contract_id: int
    date: str
    amount: float

# Insurance
class InsuranceCreate(BaseModel):
    contract_id: int
    cost: float

class InsuranceResponse(BaseModel):
    id: int
    contract_id: int
    cost: float

# Maintenance
from pydantic import BaseModel
from typing import List, Optional

# Brand
class BrandCreate(BaseModel):
    name: str

class BrandResponse(BaseModel):
    id: int
    name: str

# Model
class ModelCreate(BaseModel):
    name: str

class ModelResponse(BaseModel):
    id: int
    name: str

# Parking
class ParkingCreate(BaseModel):
    name: str

class ParkingResponse(BaseModel):
    id: int
    name: str

# Employee
class EmployeeCreate(BaseModel):
    full_name: str

class EmployeeResponse(BaseModel):
    id: int
    full_name: str

# Payment
class PaymentCreate(BaseModel):
    contract_id: int
    date: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    contract_id: int
    date: str
    amount: float

# Insurance
class InsuranceCreate(BaseModel):
    contract_id: int
    cost: float

class InsuranceResponse(BaseModel):
    id: int
    contract_id: int
    cost: float

# Maintenance
class MaintenanceCreate(BaseModel):
    car_id: int
    description: str
    date: str
    cost: float

class MaintenanceResponse(BaseModel):
    id: int
    car_id: int
    description: str
    date: str
    cost: float

# Client
class ClientCreate(BaseModel):
    full_name: str
    phone: str
    license_number: str
    birth_date: str

class ClientResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    license_number: str
    birth_date: Optional[str] = None

# Car
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

class CarResponse(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    color: str
    plate: str
    price: float

# Contract
class ContractCreate(BaseModel):
    client_id: int
    car_id: int
    start_date: str
    end_date: str
    payment_date: str
    amount: float

class ContractResponse(BaseModel):
    id: int
    client: ClientResponse
    car: CarResponse
    start_date: str
    end_date: str
    payment_date: str
    amount: Optional[float] = None
    status: str
