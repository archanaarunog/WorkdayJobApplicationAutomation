"""
Authentication service for Meta Portal API.
Handles password hashing, verification, and JWT token creation.
"""

import bcrypt
from jose import jwt
from datetime import datetime, timedelta

# JWT settings
# SECRET_KEY: Used to sign and verify JWT tokens. Must be kept secret! Change this to a strong, random value in production.
SECRET_KEY = "DittoDolly@0806"  # Replace with a secure value in production!
# ALGORITHM: The cryptographic algorithm used to sign the JWT. HS256 is a common, secure choice.
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES: How long (in minutes) the JWT token is valid before it expires.
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing

def hash_password(password: str) -> str:
    # Ensure password is not longer than 72 bytes
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password must be less than 72 bytes when encoded")
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Verify the password
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except ValueError:
        return False

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
