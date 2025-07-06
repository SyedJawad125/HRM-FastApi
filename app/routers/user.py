from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from typing import List
from app.schemas.user import UserOut
from ..schemas import LoginRequest, Token
from .. import database, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db


from app import models, schemas, utils, oauth2, database


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# router = APIRouter(tags=['Authentication'])

# routers/auth.py or similar

from fastapi import HTTPException
import traceback

@router.post("/signup", response_model=schemas.Token)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check if role exists
        role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        # Hash password
        hashed_password = utils.get_password_hash(user.password)

        # Create user
        new_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
            role_id=user.role_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Token
        access_token = oauth2.create_access_token(data={"user_id": new_user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        traceback.print_exc()  # Show error in terminal
        raise HTTPException(status_code=500, detail=str(e))



# @router.post("/login", response_model=Token)

# router = APIRouter(tags=["Authentication"])

# @router.post("/login")
# def login(user_credentials: schemas.LoginRequest, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

#     if not user or not utils.verify_password(user_credentials.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     # 🔐 Collect permissions
#     permission_names = set()

#     if user.is_superuser:
#         # Superuser: get all permissions
#         permissions = db.query(models.Permission).all()
#         permission_names = {p.name for p in permissions}
#     else:
#         # Regular user: get permissions from roles
#         for role in user.roles:
#             for permission in role.permissions:
#                 permission_names.add(permission.name)

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user_id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "permissions": list(permission_names),
#     }

@router.post("/login")
def login(user_credentials: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user or not utils.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # ✅ Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # ✅ Get only the permissions from the user's role
    if not user.role:
        raise HTTPException(status_code=400, detail="User has no role assigned")

    role = user.role  # Already linked via ForeignKey
    permissions = role.permissions  # ✅ Only permissions assigned to that role

    # ✅ Build permission list to return
    permission_list = [
        {
            "id": p.id,
            "name": p.name,
            "code": p.code,
            "description": p.description,
            "module_name": p.module_name
        }
        for p in permissions
    ]

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
        "permissions": permission_list
    }






@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db), 
             current_user: models.User = Depends(oauth2.get_current_user)):
    # Only allow users to view their own profile or admin to view any profile
    if current_user.id != id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's information"
        )
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user

@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(database.get_db), 
                 current_user: models.User = Depends(oauth2.get_current_user)):
    # Only allow admin to view all users
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can view all users"
        )
    
    users = db.query(models.User).all()
    return users

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, 
               db: Session = Depends(database.get_db), 
               current_user: models.User = Depends(oauth2.get_current_user)):
    # Only allow users to update their own profile or admin to update any profile
    if current_user.id != id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's information"
        )
    
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    
    # Hash the password if it's being updated
    if updated_user.password:
        updated_user.password = utils.hash(updated_user.password)
    
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db), 
               current_user: models.User = Depends(oauth2.get_current_user)):
    # Only allow admin to delete users or users to delete themselves
    if current_user.id != id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return