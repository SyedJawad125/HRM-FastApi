# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .database import engine, Base
# from .routers import employee, department, auth, user

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Include routers
# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(employee.router)
# app.include_router(department.router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to HRMS API"}

# @app.get("/ping")
# async def health_check():
#     return {"status": "healthy"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import employee, department, auth, user
from .models import User, Department  # Import all your models

app = FastAPI()


# Department.__table__.drop(bind=engine)
# Department.__table__.create(bind=engine)
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)

@app.get("/")
def root():
    return {"message": "Welcome to HRMS API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}