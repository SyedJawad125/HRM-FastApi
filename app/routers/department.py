from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any

from app.dependencies.permission import permission_required, require
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_departments
from fastapi.responses import JSONResponse
# from app.schemas import DepartmentListResponse


router = APIRouter(
    prefix="/departments",
    tags=['Departments']
)

# @router.get("/", response_model=List[schemas.Department])

# @router.get("/", response_model=Any)
@router.get("/", response_model=schemas.DepartmentListResponse, dependencies=[require("read_department")])
def get_departments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Department)
        query = filter_departments(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        # ✅ Convert ORM to Pydantic
        serialized_data = [schemas.Department.from_orm(dept) for dept in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Department, dependencies=[require("create_department")])
# @router.post("/", status_code=status.HTTP_201_CREATED)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # if not current_user.is_admin:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Only admin users can create departments"
        #     )

        department_data = department.dict()
        department_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_department = models.Department(**department_data)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        # return {
        #     "status": "SUCCESSFUL",
        #     "data": schemas.Department.from_orm(new_department).dict(),
        #     "message": "Department created successfully"
        # }
        return new_department

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{id}", response_model=schemas.Department, dependencies=[require("read_department")])
def get_department(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    department = db.query(models.Department).filter(models.Department.id == id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Department with id {id} not found")
    return department

@router.patch("/{id}", response_model=schemas.Department, dependencies=[require("update_department")])
def patch_update_department(
    id: int,
    updated_department: schemas.DepartmentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # if not current_user.is_admin:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Only admin users can update departments"
        #     )

        department_instance = db.query(models.Department).filter(models.Department.id == id).first()

        if not department_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with id {id} not found"
            )

        update_data = updated_department.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(department_instance, key, value)

        db.commit()
        db.refresh(department_instance)

        return department_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the department: {str(e)}"
        )


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_department(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    _: None = Depends(permission_required(["delete_department"]))
):
    department_query = db.query(models.Department).filter(models.Department.id == id)
    department = department_query.first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {id} not found"
        )

    department_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Department deleted successfully"}
