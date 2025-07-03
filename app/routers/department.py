from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, oauth2

router = APIRouter(
    prefix="/departments",
    tags=['Departments']
)

@router.get("/", response_model=List[schemas.Department])
def get_departments(db: Session = Depends(database.get_db), 
                   current_user: models.User = Depends(oauth2.get_current_user)):
    departments = db.query(models.Department).all()
    return departments

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db), 
                     current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can create departments")
    
    new_department = models.Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

@router.get("/{id}", response_model=schemas.Department)
def get_department(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    department = db.query(models.Department).filter(models.Department.id == id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Department with id {id} not found")
    return department

@router.put("/{id}", response_model=schemas.Department)
def update_department(id: int, updated_department: schemas.DepartmentCreate, 
                     db: Session = Depends(database.get_db), 
                     current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can update departments")
    
    department_query = db.query(models.Department).filter(models.Department.id == id)
    department = department_query.first()
    
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Department with id {id} not found")
    
    department_query.update(updated_department.dict(), synchronize_session=False)
    db.commit()
    return department_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(id: int, db: Session = Depends(database.get_db), 
                     current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail="Only admin users can delete departments")
    
    department_query = db.query(models.Department).filter(models.Department.id == id)
    department = department_query.first()
    
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Department with id {id} not found")
    
    department_query.delete(synchronize_session=False)
    db.commit()
    return