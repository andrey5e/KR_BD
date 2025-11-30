from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Марка автомобиля
class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Модель автомобиля
class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Модель для паркинга
class Parking(Base):
    __tablename__ = "parkings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Модель для сотрудника
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)

# Модель для платежа
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    date = Column(Date)
    amount = Column(Float)
    contract = relationship("Contract", back_populates="payments")

# Модель для страховки
class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    cost = Column(Float)
    contract = relationship("Contract", back_populates="insurances")

# Модель для истории обслуживания
class Maintenance(Base):
    __tablename__ = "maintenances"
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    description = Column(String)
    date = Column(Date)
    cost = Column(Float)
    car = relationship("Car", back_populates="maintenances")

# Модель для клиента
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone = Column(String)
    license_number = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    contracts = relationship("Contract", back_populates="client")

# Модель для автомобиля
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
