from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from .. import database, schemas, models, oauth2
from app.schemas.employee import Employee, EmployeeCreate  # Explicit imports
from app.utils import paginate_data, create_response, filter_employees
from app.dependencies.permission import permission_required, require
from app.utils import redis_client
import os, json

router = APIRouter(
    prefix="/employees",
    tags=['Employees']
)

# @router.get("/", response_model=List[schemas.Employee])
# @router.get("/", response_model=schemas.EmployeeListResponse, dependencies=[require("read_employee")])
# def get_employees(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
# ):
#     try:
#         query = db.query(models.Employee)
#         query = filter_employees(request.query_params, query)
#         data = query.all()
#         paginated_data, count = paginate_data(data, request)

#         # ✅ Convert ORM to Pydantic
#         serialized_data = [schemas.Employee.from_orm(dept) for dept in paginated_data]

#         response_data = {
#             "count": count,
#             "data": serialized_data
#         }

#         return {
#             "status": "SUCCESSFUL",
#             "result": response_data
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# redis-server.exe redis.windows.conf
# redis-cli.exe   ,     C:\Program Files\Redis



from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import json, os

from app import models, schemas, database, oauth2
from app.utils import redis_client  # ✅ Import redis_client safely

router = APIRouter()

@router.get("/", response_model=schemas.EmployeeListResponse, dependencies=[require("read_employee")])
def get_employees(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        # ✅ Create cache key using query params
        cache_key = f"employees_list:{str(request.query_params)}"

        # ✅ Try Redis cache if client exists
        if redis_client:
            cached = redis_client.get(cache_key)
            if cached:
                print("✅ Cache hit")
                cached_data = json.loads(cached)
                serialized_data = [
                    schemas.Employee(**emp) for emp in cached_data["data"]
                ]
                return {
                    "status": "SUCCESSFUL",
                    "result": {
                        "count": cached_data["count"],
                        "data": serialized_data
                    }
                }

        # ✅ DB Query
        query = db.query(models.Employee)
        query = filter_employees(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        # ✅ Convert ORM to Pydantic
        serialized_data = [schemas.Employee.from_orm(emp) for emp in paginated_data]

        # ✅ Prepare response
        response_data = {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

        # ✅ Cache response if Redis available
        if redis_client:
            # Safely get TTL from env (ignore inline comments)
            ttl_str = os.getenv("REDIS_CACHE_TTL", "300").split()[0].strip()
            ttl = int(ttl_str)
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps({
                    "count": count,
                    "data": [emp.model_dump() for emp in serialized_data]
                    }, default=str) 
                
            )

        return response_data

    except Exception as e:
        print("❌ Error in get_employees:", e)
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Employee, dependencies=[require("create_employee")])
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        

        employee_data = employee.dict()
        # department_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_employee = models.Employee(**employee_data)
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        # return {
        #     "status": "SUCCESSFUL",
        #     "data": schemas.Department.from_orm(new_department).dict(),
        #     "message": "Department created successfully"
        # }
        return new_employee

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=schemas.Employee, dependencies=[require("read_employee")])
def get_employee(id: int, db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Employee with id {id} not found")
    return employee

@router.patch("/{id}", response_model=schemas.Employee, dependencies=[require("update_employee")])
# def update_employee(id: int, updated_employee: schemas.EmployeeCreate, 
def update_employee(
    id: int,
    updated_employee: schemas.EmployeeUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        

        employee_instance = db.query(models.Employee).filter(models.Employee.id == id).first()

        if not employee_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with id {id} not found"
            )

        update_data = updated_employee.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(employee_instance, key, value)

        db.commit()
        db.refresh(employee_instance)

        return employee_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the employee: {str(e)}"
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    _: None = Depends(permission_required(["delete_employee"]))
):
    

    employee_query = db.query(models.Employee).filter(models.Employee.id == id)
    employee = employee_query.first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found"
        )

    employee_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Employee deleted successfully"}








# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from .. import database, schemas, models, oauth2
# from app.schemas.employee import Employee, EmployeeCreate  # Explicit imports

# router = APIRouter(
#     prefix="/employees",
#     tags=['Employees']
# )

# @router.get("/", response_model=List[schemas.Employee])
# def get_employees(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     employees = db.query(models.Employee).all()
#     return employees

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Employee)
# def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db), 
#                    current_user: models.User = Depends(oauth2.get_current_user)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#                            detail="Only admin users can create employees")
    
#     new_employee = models.Employee(**employee.dict())
#     db.add(new_employee)
#     db.commit()
#     db.refresh(new_employee)
#     return new_employee

# @router.get("/{id}", response_model=schemas.Employee)
# def get_employee(id: int, db: Session = Depends(database.get_db), 
#                 current_user: models.User = Depends(oauth2.get_current_user)):
#     employee = db.query(models.Employee).filter(models.Employee.id == id).first()
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Employee with id {id} not found")
#     return employee

# @router.put("/{id}", response_model=schemas.Employee)
# def update_employee(id: int, updated_employee: schemas.EmployeeCreate, 
#                    db: Session = Depends(database.get_db), 
#                    current_user: models.User = Depends(oauth2.get_current_user)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#                            detail="Only admin users can update employees")
    
#     employee_query = db.query(models.Employee).filter(models.Employee.id == id)
#     employee = employee_query.first()
    
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Employee with id {id} not found")
    
#     employee_query.update(updated_employee.dict(), synchronize_session=False)
#     db.commit()
#     return employee_query.first()

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_employee(id: int, db: Session = Depends(database.get_db), 
#                    current_user: models.User = Depends(oauth2.get_current_user)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#                            detail="Only admin users can delete employees")
    
#     employee_query = db.query(models.Employee).filter(models.Employee.id == id)
#     employee = employee_query.first()
    
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Employee with id {id} not found")
    
#     employee_query.delete(synchronize_session=False)
#     db.commit()
#     return