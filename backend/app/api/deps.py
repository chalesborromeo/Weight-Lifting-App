from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.auth import TokenData
from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.factory import PostgreSQLFactory


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )
    repo = PostgreSQLFactory.create_db_repository()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        raise credentials_exception

    user = repo.get_user(token_data.user_id, session)
    if user is None:
        raise credentials_exception

    return user


