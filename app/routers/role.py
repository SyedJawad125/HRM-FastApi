from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_roles
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/roles",
    tags=['Roles']
)

# @router.get("/", response_model=List[schemas.Department])

# @router.get("/", response_model=Any)
@router.get("/", response_model=schemas.RoleListResponse)
def get_roles(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Role)
        query = filter_roles(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        # ✅ Convert ORM to Pydantic
        serialized_data = [schemas.Role.from_orm(perms) for perms in paginated_data]

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




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Role)
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Extract permission IDs and remove them from role_data
        permission_ids = role.permission_ids or []
        role_data = role.dict(exclude={"permission_ids"})
        role_data["created_by_user_id"] = current_user.id

        # Create Role instance
        new_role = models.Role(**role_data)

        # Fetch Permission instances and assign to role
        if permission_ids:
            permissions = db.query(models.Permission).filter(models.Permission.id.in_(permission_ids)).all()
            new_role.permissions = permissions

        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        return new_role

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/{id}", response_model=schemas.Role)
def get_role(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Role with id {id} not found")
    return role

@router.patch("/{id}", response_model=schemas.Role)
def patch_update_role(
    id: int,
    updated_role: schemas.RoleUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        

        role_instance = db.query(models.Role).filter(models.Role.id == id).first()

        if not role_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {id} not found"
            )

        update_data = updated_role.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(role_instance, key, value)

        db.commit()
        db.refresh(role_instance)

        return role_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the Role: {str(e)}"
        )


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_role(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    

    role_query = db.query(models.Role).filter(models.Role.id == id)
    role = role_query.first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {id} not found"
        )

    role_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Role deleted successfully"}

