from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.models.user import User
from src.models.company import Company
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
        company_id: int = payload.get("company_id")
        user_id: int = payload.get("user_id")
        
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query user by email and validate company_id matches
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    # Additional security: verify token's company_id matches user's actual company_id
    # This prevents token reuse across different companies
    if company_id is not None and user.company_id != company_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid company context",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


# Helper function to get company context from JWT token
def get_user_company_context(token: str = Depends(oauth2_scheme)) -> dict:
    """Extract company context from JWT token without database query."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload.get("user_id"),
            "company_id": payload.get("company_id"),
            "is_admin": payload.get("is_admin", False),
            "email": payload.get("sub")
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


"""
User routes for Meta Portal API.
Handles user registration and login endpoints.
"""



# starting with /api and user tag name
router = APIRouter(prefix="/api/users", tags=["User"])

@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Get default company (users are assigned to default company by default)
    default_company = db.query(Company).filter(Company.slug == "default").first()
    if not default_company:
        raise HTTPException(status_code=500, detail="Default company not found. Please run database migration.")
    
    # Hash the password
    hashed_password = auth.hash_password(user.password)
    
    # Create user object with company assignment
    db_user = models.user.User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        company_id=default_company.id  # Assign to default company
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
    
    # Include company_id in token payload for multi-tenancy
    token_data = {
        "sub": user.email,
        "company_id": user.company_id,
        "user_id": user.id,
        "is_admin": user.is_admin
    }
    token = auth.create_access_token(token_data)
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




