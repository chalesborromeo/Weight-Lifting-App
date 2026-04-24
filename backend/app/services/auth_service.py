from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import settings
from app.db.repositories import DBRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.auth import TokenResponse, TokenData


class AuthService:
    password_hash = PasswordHash.recommended()
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, repo: DBRepository, session: Session):
        self.repo = repo
        self.session = session

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hashed password"""
        return self.password_hash.verify(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        # Query user by email
        stmt = select(User).where(User.email == email)
        user = self.session.execute(stmt).scalars().first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password):
            return None
        
        return user

    def login(self, user_login: UserLogin) -> TokenResponse:
        """Login user and return access token"""
        user = self.authenticate_user(user_login.email, user_login.password)
        
        if not user:
            raise ValueError("Invalid email or password")
        
        access_token = self.create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email
        )

    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify JWT token and return token data"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            
            if email is None:
                return None
            
            return TokenData(email=email, user_id=user_id)
        except JWTError:
            return None

    def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from token"""
        token_data = self.verify_token(token)
        
        if token_data is None:
            return None
        
        user = self.repo.get_user(token_data.user_id, self.session)
        return user

from app.core.security import create_access_token, verify_password, DUMMY_HASH, hash_password
from app.schemas.auth import LoginResponse, UserLogin, UserRegister
from app.models.user import User

class AuthService():

    def __init__(self, repo, session):
        self.repo = repo
        self.session = session

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_user_by_email(email, self.session)

        if not user:
            verify_password(password, DUMMY_HASH)
            return False
        
        if not verify_password(password, user.password):
            return False

        return user
    
    def register_user(self, user: UserRegister):
        new_user = User()
        new_user.email = user.email
        new_user.password = hash_password(user.password)

        self.repo.save_user(new_user, self.session)
        self.session.refresh(new_user)

        token = create_access_token({"sub": str(new_user.id)})
        return LoginResponse(access_token=token, token_type="bearer", user=new_user)
    

    def login_user(self, credentials: UserLogin):
        user = self.authenticate_user(credentials.email, credentials.password)
        if not user:
            return None
        
        token = create_access_token({"sub": str(user.id)})
        return LoginResponse(access_token=token, token_type="bearer",user=user)

        
