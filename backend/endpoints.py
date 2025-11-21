from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import SessionLocal
from models import (
    Brand, Model, Parking, Employee, Payment, Insurance, Maintenance, Client, Car, Contract
)
from schemas import (
    BrandCreate, BrandResponse, ModelCreate, ModelResponse, ParkingCreate, ParkingResponse,
    EmployeeCreate, EmployeeResponse, PaymentCreate, PaymentResponse, InsuranceCreate, InsuranceResponse,
    MaintenanceCreate, MaintenanceResponse, ClientCreate, ClientResponse, CarCreate, CarUpdate, CarResponse,
    ContractCreate, ContractResponse
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Brand Endpoints
@router.get("/brands", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()

@router.post("/brands", response_model=BrandResponse)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    existing = db.query(Brand).filter(Brand.name == brand.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Brand already exists")
    db_brand = Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.put("/brands/{brand_id}", response_model=BrandResponse)
def update_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    db_brand.name = brand.name
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.delete("/brands/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    db.delete(db_brand)
    db.commit()
    return {"message": "Brand deleted"}

# Model Endpoints
@router.get("/models", response_model=List[ModelResponse])
def get_models(db: Session = Depends(get_db)):
    return db.query(Model).all()

@router.post("/models", response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    existing = db.query(Model).filter(Model.name == model.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Model already exists")
    db_model = Model(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.put("/models/{model_id}", response_model=ModelResponse)
def update_model(model_id: int, model: ModelCreate, db: Session = Depends(get_db)):
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    db_model.name = model.name
    db.commit()
    db.refresh(db_model)
    return db_model

@router.delete("/models/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(db_model)
    db.commit()
    return {"message": "Model deleted"}

# Parking Endpoints
@router.get("/parkings", response_model=List[ParkingResponse])
def get_parkings(db: Session = Depends(get_db)):
    return db.query(Parking).all()

@router.post("/parkings", response_model=ParkingResponse)
def create_parking(parking: ParkingCreate, db: Session = Depends(get_db)):
    db_parking = Parking(**parking.dict())
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking

@router.put("/parkings/{parking_id}", response_model=ParkingResponse)
def update_parking(parking_id: int, parking: ParkingCreate, db: Session = Depends(get_db)):
    db_parking = db.query(Parking).filter(Parking.id == parking_id).first()
    if not db_parking:
        raise HTTPException(status_code=404, detail="Parking not found")
    db_parking.name = parking.name
    db.commit()
    db.refresh(db_parking)
    return db_parking

@router.delete("/parkings/{parking_id}")
def delete_parking(parking_id: int, db: Session = Depends(get_db)):
    db_parking = db.query(Parking).filter(Parking.id == parking_id).first()
    if not db_parking:
        raise HTTPException(status_code=404, detail="Parking not found")
    db.delete(db_parking)
    db.commit()
    return {"message": "Parking deleted"}

# Employee Endpoints
@router.get("/employees", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db_employee.full_name = employee.full_name
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted"}

# Payment Endpoints
@router.get("/payments", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return [
        PaymentResponse(
            id=p.id,
            contract_id=p.contract_id,
            date=str(p.date),
            amount=p.amount
        ) for p in payments
    ]

@router.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == payment.contract_id).first()
    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")
    db_payment = Payment(
        contract_id=payment.contract_id,
        date=date.fromisoformat(payment.date),
        amount=payment.amount
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return PaymentResponse(
        id=db_payment.id,
        contract_id=db_payment.contract_id,
        date=str(db_payment.date),
        amount=db_payment.amount
    )

@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    contract = db.query(Contract).filter(Contract.id == payment.contract_id).first()
    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")
    db_payment.contract_id = payment.contract_id
    db_payment.date = date.fromisoformat(payment.date)
    db_payment.amount = payment.amount
    db.commit()
    db.refresh(db_payment)
    return PaymentResponse(
        id=db_payment.id,
        contract_id=db_payment.contract_id,
        date=str(db_payment.date),
        amount=db_payment.amount
    )

@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return {"message": "Payment deleted"}

# Insurance Endpoints
@router.get("/insurances", response_model=List[InsuranceResponse])
def get_insurances(db: Session = Depends(get_db)):
    insurances = db.query(Insurance).all()
    return [
        InsuranceResponse(
            id=i.id,
            contract_id=i.contract_id,
            cost=i.cost
        ) for i in insurances
    ]

@router.post("/insurances", response_model=InsuranceResponse)
def create_insurance(insurance: InsuranceCreate, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == insurance.contract_id).first()
    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")
    db_insurance = Insurance(
        contract_id=insurance.contract_id,
        cost=insurance.cost
    )
    db.add(db_insurance)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance

@router.put("/insurances/{insurance_id}", response_model=InsuranceResponse)
def update_insurance(insurance_id: int, insurance: InsuranceCreate, db: Session = Depends(get_db)):
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    contract = db.query(Contract).filter(Contract.id == insurance.contract_id).first()
    if not contract:
        raise HTTPException(status_code=400, detail="Contract not found")
    db_insurance.contract_id = insurance.contract_id
    db_insurance.cost = insurance.cost
    db.commit()
    db.refresh(db_insurance)
    return db_insurance

@router.delete("/insurances/{insurance_id}")
def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
    if not db_insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    db.delete(db_insurance)
    db.commit()
    return {"message": "Insurance deleted"}

# Maintenance Endpoints
