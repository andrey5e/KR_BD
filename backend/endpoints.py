from datetime import date
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from .database import get_db
from .models import (
    Brand, Model, Parking, Employee, Payment, Insurance, Maintenance, Client, Car, Contract
)

from .schemas import (
    BrandCreate, BrandResponse, ModelCreate, ModelResponse, ParkingCreate, ParkingResponse,
    EmployeeCreate, EmployeeResponse, PaymentCreate, PaymentResponse,
    ClientResponse, ClientCreate, CarResponse, CarCreate, CarUpdate,
    ContractResponse, ContractCreate, InsuranceCreate, InsuranceResponse,
    MaintenanceCreate, MaintenanceResponse
)

# Эндпоинты для марок автомобилей
def setup_brand_endpoints(app):
    @app.get("/brands", response_model=List[BrandResponse])
    def get_brands(db: Session = Depends(get_db)):
        return db.query(Brand).all()

    @app.post("/brands", response_model=BrandResponse)
    def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
        existing = db.query(Brand).filter(Brand.name == brand.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Brand already exists")
        db_brand = Brand(**brand.dict())
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand

    @app.put("/brands/{brand_id}", response_model=BrandResponse)
    def update_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not db_brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        db_brand.name = brand.name
        db.commit()
        db.refresh(db_brand)
        return db_brand

    @app.delete("/brands/{brand_id}")
    def delete_brand(brand_id: int, db: Session = Depends(get_db)):
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not db_brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        db.delete(db_brand)
        db.commit()
        return {"message": "Brand deleted"}

# Эндпоинты для моделей автомобилей
def setup_model_endpoints(app):
    @app.get("/models", response_model=List[ModelResponse])
    def get_models(db: Session = Depends(get_db)):
        return db.query(Model).all()

    @app.post("/models", response_model=ModelResponse)
    def create_model(model: ModelCreate, db: Session = Depends(get_db)):
        existing = db.query(Model).filter(Model.name == model.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Model already exists")
        db_model = Model(**model.dict())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @app.put("/models/{model_id}", response_model=ModelResponse)
    def update_model(model_id: int, model: ModelCreate, db: Session = Depends(get_db)):
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")
        db_model.name = model.name
        db.commit()
        db.refresh(db_model)
        return db_model

    @app.delete("/models/{model_id}")
    def delete_model(model_id: int, db: Session = Depends(get_db)):
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")
        db.delete(db_model)
        db.commit()
        return {"message": "Model deleted"}

# Эндпоинты для паркингов
def setup_parking_endpoints(app):
    @app.get("/parkings", response_model=List[ParkingResponse])
    def get_parkings(db: Session = Depends(get_db)):
        return db.query(Parking).all()

    @app.post("/parkings", response_model=ParkingResponse)
    def create_parking(parking: ParkingCreate, db: Session = Depends(get_db)):
        existing = db.query(Parking).filter(Parking.name == parking.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Parking already exists")
        db_parking = Parking(**parking.dict())
        db.add(db_parking)
        db.commit()
        db.refresh(db_parking)
        return db_parking

    @app.put("/parkings/{parking_id}", response_model=ParkingResponse)
    def update_parking(parking_id: int, parking: ParkingCreate, db: Session = Depends(get_db)):
        db_parking = db.query(Parking).filter(Parking.id == parking_id).first()
        if not db_parking:
            raise HTTPException(status_code=404, detail="Parking not found")
        db_parking.name = parking.name
        db.commit()
        db.refresh(db_parking)
        return db_parking

    @app.delete("/parkings/{parking_id}")
    def delete_parking(parking_id: int, db: Session = Depends(get_db)):
        db_parking = db.query(Parking).filter(Parking.id == parking_id).first()
        if not db_parking:
            raise HTTPException(status_code=404, detail="Parking not found")
        db.delete(db_parking)
        db.commit()
        return {"message": "Parking deleted"}

# Эндпоинты для сотрудников
def setup_employee_endpoints(app):
    @app.get("/employees", response_model=List[EmployeeResponse])
    def get_employees(db: Session = Depends(get_db)):
        return db.query(Employee).all()

    @app.post("/employees", response_model=EmployeeResponse)
    def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
        existing = db.query(Employee).filter(Employee.full_name == employee.full_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Employee already exists")
        db_employee = Employee(**employee.dict())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    @app.put("/employees/{employee_id}", response_model=EmployeeResponse)
    def update_employee(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
        db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        db_employee.full_name = employee.full_name
        db.commit()
        db.refresh(db_employee)
        return db_employee

    @app.delete("/employees/{employee_id}")
    def delete_employee(employee_id: int, db: Session = Depends(get_db)):
        db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        db.delete(db_employee)
        db.commit()
        return {"message": "Employee deleted"}

# Эндпоинты для платежей
def setup_payment_endpoints(app):
    @app.get("/payments", response_model=List[PaymentResponse])
    def get_payments(db: Session = Depends(get_db)):
        return db.query(Payment).all()

    @app.post("/payments", response_model=PaymentResponse)
    def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
        # Проверка существования договора
        contract = db.query(Contract).filter(Contract.id == payment.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    @app.put("/payments/{payment_id}", response_model=PaymentResponse)
    def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        db_payment.contract_id = payment.contract_id
        db_payment.date = date.fromisoformat(payment.date)
        db_payment.amount = payment.amount
        db.commit()
        db.refresh(db_payment)
        return db_payment

    @app.delete("/payments/{payment_id}")
    def delete_payment(payment_id: int, db: Session = Depends(get_db)):
        db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        db.delete(db_payment)
        db.commit()
        return {"message": "Payment deleted"}

# Эндпоинты для страховок
def setup_insurance_endpoints(app):
    @app.get("/insurances", response_model=List[InsuranceResponse])
    def get_insurances(db: Session = Depends(get_db)):
        insurances = db.query(Insurance).options(joinedload(Insurance.contract).joinedload(Contract.client), joinedload(Insurance.contract).joinedload(Contract.car)).all()
        return [
            InsuranceResponse(
                id=i.id,
                contract=ContractResponse(
                    id=i.contract.id,
                    client=ClientResponse(
                        id=i.contract.client.id,
                        full_name=i.contract.client.full_name,
                        phone=i.contract.client.phone,
                        license_number=i.contract.client.license_number,
                        birth_date=str(i.contract.client.birth_date) if i.contract.client.birth_date else None
                    ),
                    car=CarResponse(
                        id=i.contract.car.id,
                        brand=i.contract.car.brand,
                        model=i.contract.car.model,
                        year=i.contract.car.year,
                        color=i.contract.car.color,
                        license_plate=i.contract.car.plate,
                        price=i.contract.car.price
                    ),
                    start_date=str(i.contract.start_date),
                    end_date=str(i.contract.end_date),
                    payment_date=str(i.contract.payment_date),
                    amount=i.contract.amount,
                    status=i.contract.status
                ),
                cost=i.cost
            ) for i in insurances
        ]

    @app.post("/insurances", response_model=InsuranceResponse)
    def create_insurance(insurance: InsuranceCreate, db: Session = Depends(get_db)):
        contract = db.query(Contract).filter(Contract.id == insurance.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        db_insurance = Insurance(**insurance.dict())
        db.add(db_insurance)
        db.commit()
        db.refresh(db_insurance)
        # Возвращаем полный объект с joinedload
        full_insurance = db.query(Insurance).options(joinedload(Insurance.contract).joinedload(Contract.client), joinedload(Insurance.contract).joinedload(Contract.car)).filter(Insurance.id == db_insurance.id).first()
        return InsuranceResponse(
            id=full_insurance.id,
            contract=ContractResponse(
                id=full_insurance.contract.id,
                client=ClientResponse(
                    id=full_insurance.contract.client.id,
                    full_name=full_insurance.contract.client.full_name,
                    phone=full_insurance.contract.client.phone,
                    license_number=full_insurance.contract.client.license_number,
                    birth_date=str(full_insurance.contract.client.birth_date) if full_insurance.contract.client.birth_date else None
                ),
                car=CarResponse(
                    id=full_insurance.contract.car.id,
                    brand=full_insurance.contract.car.brand,
                    model=full_insurance.contract.car.model,
                    year=full_insurance.contract.car.year,
                    color=full_insurance.contract.car.color,
                    license_plate=full_insurance.contract.car.plate,
                    price=full_insurance.contract.car.price
                ),
                start_date=str(full_insurance.contract.start_date),
                end_date=str(full_insurance.contract.end_date),
                payment_date=str(full_insurance.contract.payment_date),
                amount=full_insurance.contract.amount,
                status=full_insurance.contract.status
            ),
            cost=full_insurance.cost
        )

    @app.put("/insurances/{insurance_id}", response_model=InsuranceResponse)
    def update_insurance(insurance_id: int, insurance: InsuranceCreate, db: Session = Depends(get_db)):
        db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not db_insurance:
            raise HTTPException(status_code=404, detail="Insurance not found")
        db_insurance.contract_id = insurance.contract_id
        db_insurance.cost = insurance.cost
        db.commit()
        db.refresh(db_insurance)
        # Возвращаем полный объект
        full_insurance = db.query(Insurance).options(joinedload(Insurance.contract).joinedload(Contract.client), joinedload(Insurance.contract).joinedload(Contract.car)).filter(Insurance.id == db_insurance.id).first()
        return InsuranceResponse(
            id=full_insurance.id,
            contract=ContractResponse(
                id=full_insurance.contract.id,
                client=ClientResponse(
                    id=full_insurance.contract.client.id,
                    full_name=full_insurance.contract.client.full_name,
                    phone=full_insurance.contract.client.phone,
                    license_number=full_insurance.contract.client.license_number,
                    birth_date=str(full_insurance.contract.client.birth_date) if full_insurance.contract.client.birth_date else None
                ),
                car=CarResponse(
                    id=full_insurance.contract.car.id,
                    brand=full_insurance.contract.car.brand,
                    model=full_insurance.contract.car.model,
                    year=full_insurance.contract.car.year,
                    color=full_insurance.contract.car.color,
                    license_plate=full_insurance.contract.car.plate,
                    price=full_insurance.contract.car.price
                ),
                start_date=str(full_insurance.contract.start_date),
                end_date=str(full_insurance.contract.end_date),
                payment_date=str(full_insurance.contract.payment_date),
                amount=full_insurance.contract.amount,
                status=full_insurance.contract.status
            ),
            cost=full_insurance.cost
        )

    @app.delete("/insurances/{insurance_id}")
    def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
        db_insurance = db.query(Insurance).filter(Insurance.id == insurance_id).first()
        if not db_insurance:
            raise HTTPException(status_code=404, detail="Insurance not found")
        db.delete(db_insurance)
        db.commit()
        return {"message": "Insurance deleted"}
