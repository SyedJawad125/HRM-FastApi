from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import attendance

from .database import engine, Base
from .routers import employee, department, auth, user, role, permission, rank, attendance, timesheet, leave             
from .models import User, Department  # All models, if needed

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(rank.router)
app.include_router(attendance.router)
app.include_router(timesheet.router)
app.include_router(leave.router)
app.include_router(permission.router)  # ✅ FIXED
app.include_router(role.router)

@app.get("/")
def root():
    return {"message": "Welcome to HRMS API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}
