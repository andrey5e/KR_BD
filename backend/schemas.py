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
