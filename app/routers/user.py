from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from typing import List
from app.schemas.user import UserOut
from ..schemas import LoginRequest, Token
from .. import database, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# router = APIRouter(tags=['Authentication'])

@router.post("/signup", response_model=schemas.Token)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = utils.get_password_hash(user.hashed_password)
    
    # Create new user
    new_user = models.User(
        email=user.email,
        password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate access token
    access_token = oauth2.create_access_token(data={"user_id": new_user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


# router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: LoginRequest, db: Session = Depends(database.get_db)):
    # Lookup user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Check password
    if not utils.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Create JWT token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


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