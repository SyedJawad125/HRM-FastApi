from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_departments

router = APIRouter(
    prefix="/departments",
    tags=['Departments']
)

# @router.get("/", response_model=List[schemas.Department])

@router.get("/", response_model=Any)
def get_departments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        # Step 1: Get all departments
        query = db.query(models.Department)

        # Step 2: Apply filters from query params (if needed)
        query = filter_departments(request.query_params, query)  # You need to write this helper

        # Step 3: Get filtered results
        data = query.all()

        # Step 4: Apply pagination
        paginated_data, count = paginate_data(data, request)

        # Step 5: Serialize the paginated data
        serialized_data = [schemas.Department.from_orm(dept).dict() for dept in paginated_data]

        # Step 6: Build the response
        response_data = {
            "count": count,
            "data": serialized_data,
        }
        # return create_response(response_data, "SUCCESSFUL", 200)
        return {
                "status": "SUCCESSFUL",
                "result": response_data
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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