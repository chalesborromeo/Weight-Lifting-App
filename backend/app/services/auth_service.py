
from app.core.security import create_access_token, verify_password, DUMMY_HASH, hash_password
from app.schemas.auth import LoginResponse, UserLogin, UserRegister
from app.models.user import User

class AuthService:

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

        
