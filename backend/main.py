from fastapi import FastAPI
import uvicorn

from database import engine
from models import Base
from endpoints import router

# Создание таблиц
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
