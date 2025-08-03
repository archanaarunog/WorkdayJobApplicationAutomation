"""
Authentication service for Meta Portal API.
Handles password hashing, verification, and JWT token creation.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Password hashing context
# This sets up a secure way to hash and verify passwords using the bcrypt algorithm.
# Bcrypt is an industry-standard, secure way to store passwords (never store plain passwords!).
# 'deprecated="auto"' means older algorithms will be marked as deprecated if added in the future.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
# SECRET_KEY: Used to sign and verify JWT tokens. Must be kept secret! Change this to a strong, random value in production.
SECRET_KEY = "DittoDolly@0806"  # Replace with a secure value in production!
# ALGORITHM: The cryptographic algorithm used to sign the JWT. HS256 is a common, secure choice.
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES: How long (in minutes) the JWT token is valid before it expires.
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing

# Hashes a plain text password using bcrypt and returns the hashed password.
# Parameters:
#   password (str): The user's plain text password to be hashed.
# Returns:
#   str: The hashed password, safe to store in the database.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifies that a plain text password matches the stored hashed password.
# Parameters:
#   plain_password (str): The password entered by the user.
#   hashed_password (str): The hashed password from the database.
# Returns:
#   bool: True if the password matches, False otherwise.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation

# Creates a JWT (JSON Web Token) for user authentication.
# Parameters:
#   data (dict): The data to encode in the token (e.g., user info).
#   expires_delta (int): How many minutes until the token expires (default: 60).
# Returns:
#   str: The encoded JWT token as a string.
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
