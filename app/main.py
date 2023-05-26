from fastapi import FastAPI
from app.routers import pdf
from .routers import email,users,auth,profile
from app import models
from app.database import engine

app = FastAPI()

# cretes all tables
# models.Base.metadata.create_all(bind=engine)

app.include_router(email.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(pdf.router)