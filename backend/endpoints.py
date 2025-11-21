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
@router.get("/maintenances", response_model=List[MaintenanceResponse])
def get_maintenances(db: Session = Depends(get_db)):
    maintenances = db.query(Maintenance).all()
    return [
        MaintenanceResponse(
            id=m.id,
            car_id=m.car_id,
            description=m.description,
            date=str(m.date),
            cost=m.cost
        ) for m in maintenances
    ]

@router.post("/maintenances", response_model=MaintenanceResponse)
def create_maintenance(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == maintenance.car_id).first()
    if not car:
        raise HTTPException(status_code=400, detail="Car not found")
    db_maintenance = Maintenance(
        car_id=maintenance.car_id,
        description=maintenance.description,
        date=date.fromisoformat(maintenance.date),
        cost=maintenance.cost
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return MaintenanceResponse(
        id=db_maintenance.id,
        car_id=db_maintenance.car_id,
        description=db_maintenance.description,
        date=str(db_maintenance.date),
        cost=db_maintenance.cost
    )

@router.put("/maintenances/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(maintenance_id: int, maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    car = db.query(Car).filter(Car.id == maintenance.car_id).first()
    if not car:
        raise HTTPException(status_code=400, detail="Car not found")
    db_maintenance.car_id = maintenance.car_id
    db_maintenance.description = maintenance.description
    db_maintenance.date = date.fromisoformat(maintenance.date)
    db_maintenance.cost = maintenance.cost
    db.commit()
    db.refresh(db_maintenance)
    return MaintenanceResponse(
        id=db_maintenance.id,
        car_id=db_maintenance.car_id,
        description=db_maintenance.description,
        date=str(db_maintenance.date),
        cost=db_maintenance.cost
    )

@router.delete("/maintenances/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    db.delete(db_maintenance)
    db.commit()
    return {"message": "Maintenance deleted"}

# Client Endpoints
@router.get("/clients", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return [
        ClientResponse(
            id=c.id,
            full_name=c.full_name,
            phone=c.phone,
            license_number=c.license_number,
            birth_date=str(c.birth_date) if c.birth_date else None
        ) for c in clients
    ]

@router.post("/clients", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.license_number == client.license_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client with this license number already exists")
    db_client = Client(
        full_name=client.full_name,
        phone=client.phone,
        license_number=client.license_number,
        birth_date=date.fromisoformat(client.birth_date)
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return ClientResponse(
        id=db_client.id,
        full_name=db_client.full_name,
        phone=db_client.phone,
        license_number=db_client.license_number,
        birth_date=str(db_client.birth_date) if db_client.birth_date else None
    )

@router.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    existing = db.query(Client).filter(Client.license_number == client.license_number).first()
    if existing and existing.id != client_id:
        raise HTTPException(status_code=400, detail="License number already exists")
    db_client.full_name = client.full_name
    db_client.phone = client.phone
    db_client.license_number = client.license_number
    db_client.birth_date = date.fromisoformat(client.birth_date)
    db.commit()
    db.refresh(db_client)
    return ClientResponse(
        id=db_client.id,
        full_name=db_client.full_name,
        phone=db_client.phone,
        license_number=db_client.license_number,
        birth_date=str(db_client.birth_date) if db_client.birth_date else None
    )

@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted"}

# Car Endpoints
@router.get("/cars", response_model=List[CarResponse])
def get_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()

@router.post("/cars", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    existing = db.query(Car).filter(Car.plate == car.plate).first()
    if existing:
        raise HTTPException(status_code=400, detail="Car with this plate already exists")
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.put("/cars/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    existing = db.query(Car).filter(Car.plate == car.plate).first()
    if existing and existing.id != car_id:
        raise HTTPException(status_code=400, detail="Plate already exists")
    db_car.color = car.color
    db_car.plate = car.plate
    db_car.price = car.price
    db.commit()
    db.refresh(db_car)
    return db_car

@router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}

# Contract Endpoints
@router.get("/contracts", response_model=List[ContractResponse])
def get_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).options(joinedload(Contract.client), joinedload(Contract.car)).all()
    return contracts  # Pydantic обработает nested и даты

@router.post("/contracts", response_model=ContractResponse)
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == contract.client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client not found")
    car = db.query(Car).filter(Car.id == contract.car_id).first()
    if not car:
        raise HTTPException(status_code=400, detail="Car not found")
    # Проверяем, не арендована ли машина уже (упрощённо, без учёта дат)
    existing_contract = db.query(Contract).filter(Contract.car_id == contract.car_id, Contract.status == "active").first()
    if existing_contract:
        raise HTTPException(status_code=400, detail="Car is already rented")
    db_contract = Contract(
        client_id=contract.client_id,
        car_id=contract.car_id,
        start_date=date.fromisoformat(contract.start_date),
        end_date=date.fromisoformat(contract.end_date),
        payment_date=date.fromisoformat(contract.payment_date),
        amount=contract.amount
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    db_contract = db.query(Contract).options(joinedload(Contract.client), joinedload(Contract.car)).filter(Contract.id == db_contract.id).first()
    return db_contract  # Для nested

@router.put("/contracts/{contract_id}", response_model=ContractResponse)
def update_contract(contract_id: int, contract: ContractCreate, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    client = db.query(Client).filter(Client.id == contract.client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client not found")
    car = db.query(Car).filter(Car.id == contract.car_id).first()
    if not car:
        raise HTTPException(status_code=400, detail="Car not found")
    db_contract.client_id = contract.client_id
    db_contract.car_id = contract.car_id
    db_contract.start_date = date.fromisoformat(contract.start_date)
    db_contract.end_date = date.fromisoformat(contract.end_date)
    db_contract.payment_date = date.fromisoformat(contract.payment_date)
    db_contract.amount = contract.amount
    db.commit()
    db.refresh(db_contract)
    db_contract = db.query(Contract).options(joinedload(Contract.client), joinedload(Contract.car)).filter(Contract.id == db_contract.id).first()
    return db_contract

@router.delete("/contracts/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(db_contract)
    db.commit()
    return {"message": "Contract deleted"}
