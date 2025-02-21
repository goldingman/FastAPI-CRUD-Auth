from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# Security configs
SECRET_KEY = "your-secret-key-here"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["authentication"])


class Token(BaseModel):
    """Schema for the authentication token response."""
    access_token: str
    token_type: str

    def is_active(self):
        """Check if user is active."""
        return not self.disabled

    def to_dict(self):
        """Convert token to dictionary."""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type
        }


class User(BaseModel):
    """Schema for user information."""
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = False

    def is_active(self):
        """Check if user is active."""
        return not self.disabled

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "disabled": self.disabled
        }


class UserInDB(User):
    """Schema for user information stored in database."""
    hashed_password: str

    def verify_password(self, password: str):
        """Verify password matches hash."""
        return pwd_context.verify(password, self.hashed_password)


# Simulate user database
fake_users_db = {}


def verify_password(plain_password, hashed_password):
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Get password hash."""
    return pwd_context.hash(password)


def get_user(username: str):
    """Get user from database."""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def create_access_token(data: dict):
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register")
async def register(username: str, email: str, password: str):
    """Register a new user."""
    if username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password
    }
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token."""
    user = get_user(form_data.username)
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
