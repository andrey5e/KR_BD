from datetime import date
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, joinedload

DATABASE_URL = "postgresql://postgres:/rental_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Марка
class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Модель
class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Паркинг
class Parking(Base):
    __tablename__ = "parkings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Сотрудник
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)

# Платёж
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    date = Column(Date)
    amount = Column(Float)
    contract = relationship("Contract", back_populates="payments")

# Страховка
class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    cost = Column(Float)
    contract = relationship("Contract", back_populates="insurances")

# История обслуживания
class Maintenance(Base):
    __tablename__ = "maintenances"
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    description = Column(String)
    date = Column(Date)
    cost = Column(Float)
    car = relationship("Car", back_populates="maintenances")

# Клиент
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone = Column(String)
    license_number = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    contracts = relationship("Contract", back_populates="client")

# Автомобиль
class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    color = Column(String)
    plate = Column(String, unique=True, index=True)
    price = Column(Float)
    maintenances = relationship("Maintenance", back_populates="car")
    contracts = relationship("Contract", back_populates="car")

# Договор
class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    payment_date = Column(Date)
    amount = Column(Float)
    status = Column(String, default="active")
    client = relationship("Client", back_populates="contracts")
    car = relationship("Car", back_populates="contracts")
    payments = relationship("Payment", back_populates="contract")
    insurances = relationship("Insurance", back_populates="contract")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
