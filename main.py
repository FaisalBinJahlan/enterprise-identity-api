from fastapi import FastAPI
from api.admin import router as admin_router
from api.auth import router as auth_router
from api.health import router as health_router
from core.database import Base, engine
from models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Identity API",
    description="Secure authentication and authorization API with RBAC.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(admin_router)
