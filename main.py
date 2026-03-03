
from fastapi import FastAPI
from src.interfaces.api.routes import router

app = FastAPI(title="Fintech Transaction System")
app.include_router(router)
