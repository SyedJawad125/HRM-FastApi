from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, oauth2
from app.schemas.employee import Employee, EmployeeCreate  # Explicit imports

router = APIRouter(
    prefix="/employees",
    tags=['Employees']
)

@router.get("/", response_model=List[schemas.Employee])
def get_employees(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    employees = db.query(models.Employee).all()
    return employees

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can create employees")
    
    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/{id}", response_model=schemas.Employee)
def get_employee(id: int, db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Employee with id {id} not found")
    return employee

@router.put("/{id}", response_model=schemas.Employee)
def update_employee(id: int, updated_employee: schemas.EmployeeCreate, 
                   db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can update employees")
    
    employee_query = db.query(models.Employee).filter(models.Employee.id == id)
    employee = employee_query.first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Employee with id {id} not found")
    
    employee_query.update(updated_employee.dict(), synchronize_session=False)
    db.commit()
    return employee_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can delete employees")
    
    employee_query = db.query(models.Employee).filter(models.Employee.id == id)
    employee = employee_query.first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Employee with id {id} not found")
    
    employee_query.delete(synchronize_session=False)
    db.commit()
    return