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



from sqlalchemy.orm import joinedload

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    print("🔐 get_current_user called")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # Load all permissions
    all_permissions = db.query(models.Permission).all()
    permissions_dict = {perm.code: False for perm in all_permissions}

    # Determine permissions based on role or superuser
    if user.is_superuser and not user.role:
        # Superuser with no role: full access
        for perm in all_permissions:
            permissions_dict[perm.code] = True
    elif user.role:
        for perm in user.role.permissions:
            permissions_dict[perm.code] = True
    else:
        # No role, not superuser = invalid setup
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no role assigned"
        )

    # Attach to user for permission checks
    user.permissions_dict = permissions_dict

    return user





# from datetime import datetime, timedelta
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session
# from . import models, database
# from .config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

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

#         # ✅ Fetch full user from database
#         user = db.query(models.User).filter(models.User.id == user_id).first()
#         if not user:
#             raise credentials_exception

#         # ✅ Attach permissions (build dictionary if needed)
#         if not user.is_superuser:
#             user.permissions = {
#                 perm.code: True for role in user.roles for perm in role.permissions
#             }
#         else:
#             user.permissions = {}  # Superuser skips permission checks

#         return user

#     except JWTError:
#         raise credentials_exception
