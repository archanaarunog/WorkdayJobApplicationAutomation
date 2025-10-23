from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.models.user import User
from src.config.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src import schemas, models
from src.services import auth
# OAuth2 scheme for extracting token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# IMPORTANT: Use the same secret key and algorithm as your auth service
SECRET_KEY = "DittoDolly@0806"  # Must match src/services/auth.py
ALGORITHM = "HS256"

# Dependency to get the current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
"""
User routes for Meta Portal API.
Handles user registration and login endpoints.
"""



# starting with /api and user tag name
router = APIRouter(prefix="/api/users", tags=["User"])

[]
@router.post("/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the password
    hashed_password = auth.hash_password(user.password)
    # Create user object
    db_user = models.user.User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(form: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == form.email).first()
    if not user or not auth.verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile information.
    """
    return current_user

@router.patch("/me", response_model=schemas.UserRead)
def update_current_user_profile(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the current authenticated user's profile information.
    Only provided fields will be updated.
    """
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user




