import jwt
from jwt import ExpiredSignatureError

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.user_schema import UserRead
from app.user.user_service import user_service
from app.auth.auth_schema import Token, TokenUser
from common.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
DpOauth2Scheme = Annotated[str, Depends(oauth2_scheme)]

class AuthService:
    @staticmethod
    async def authenticate_user(db: AsyncSession, username_or_email: str, password: str) -> Optional[UserRead]:
        return await user_service.validate_password(db, username_or_email, password)

    @staticmethod
    def create_access_token(user: UserRead, expires_delta: timedelta | None = None) -> Token | None:
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        exp_time = datetime.now(timezone.utc) + expires_delta

        try:
            token_user = TokenUser(
                id=user.id,
                full_name=user.full_name,   
                username=user.username,
                email=user.email,
                exp=exp_time,
                reset_password=user.force_password_change
            )

            encoded_jwt = jwt.encode(token_user.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            return Token(access_token=encoded_jwt, token_type="bearer")
        except Exception as e:
            print(f"Error creating access token: {e}")
            return None

    @staticmethod
    def decode_token(token: str) -> TokenUser:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenUser.model_validate(payload)


auth_service = AuthService()

def get_current_user(token: DpOauth2Scheme) -> TokenUser:
    try:
        return auth_service.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token", headers={"error-code": "token_expired"})

DpCurrentUser = Annotated[TokenUser, Depends(get_current_user)]