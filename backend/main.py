from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .database import engine, metadata
from .endpoints import (
    setup_brand_endpoints,
    setup_model_endpoints,
    setup_parking_endpoints,
    setup_employee_endpoints,
    setup_payment_endpoints,
    setup_insurance_endpoints,
    setup_maintenance_endpoints,
    setup_client_endpoints,
    setup_car_endpoints,
    setup_contract_endpoints,
)

# Создание FastAPI-приложения
app = FastAPI(
    title="Car Rental API",
    description="Прокат автомобилей"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание всех таблиц в базе данных (если они ещё не созданы)
metadata.create_all(bind=engine)

# Регистрация всех эндпоинтов
setup_brand_endpoints(app)
setup_model_endpoints(app)
setup_parking_endpoints(app)
setup_employee_endpoints(app)
setup_payment_endpoints(app)
setup_insurance_endpoints(app)
setup_maintenance_endpoints(app)
setup_client_endpoints(app)
setup_car_endpoints(app)
setup_contract_endpoints(app)

# Корневой эндпоинт для проверки
@app.get("/")
def root():
    return {"message": "Welcome to the Car Rental API! Use /docs for interactive documentation."}

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
