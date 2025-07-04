# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from . import schemas, database, models
# from sqlalchemy.orm import Session
# from .config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
    
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("user_id")
        
#         if user_id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id=user_id)
#     except JWTError:
#         raise credentials_exception
        
#     return token_data

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     token = verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.id == token.id).first()
    
#     return user



# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from app.config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("user_id")
#         if user_id is None:
#             raise credentials_exception
#         return payload
#     except JWTError:
#         raise credentials_exception

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_access_token(token, credentials_exception)



# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session
# from . import models, database
# from .config import settings

# # Define OAuth2 scheme
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # JWT configuration
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM

# # Function to get the current user based on the JWT token
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise credentials_exception
#     return user



from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import models, database
from .config import settings

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Function to create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get the current user based on the JWT token
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise credentials_exception
#     return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    print("🔐 get_current_user called")  # Check if function is entered

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print("🔍 Decoding token:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Token decoded:", payload)
        user_id: int = payload.get("user_id")
        if user_id is None:
            print("⚠️ user_id missing from payload")
            raise credentials_exception
    except JWTError as e:
        print("❌ JWT Error:", str(e))
        raise credentials_exception

    print("🧠 Fetching user from DB...")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print("👤 Fetched user:", user)

    if user is None:
        raise credentials_exception

    return user
