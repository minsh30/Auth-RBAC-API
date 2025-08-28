#/core/deps.py

from fastapi import Depends, HTTPException, status 
from fastapi.security import HTTPBearer          #Reads "Authorization: Bearer <Token>"
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from app.db.session import get_session
from app.db.models import User, Role, UserRole
from app.core.security import decode_token

#security scheme that extracts bearer token from header
bearer = HTTPBearer()

async def current_user(
    token = Depends(bearer),                      # get token from header
    db: AsyncSession = Depends(get_session)       # DB session
) -> User:
    """Resolve the current user  from a valid  JWT token"""
    
    try:
        email = decode_token(token.credentials) #will raise invalid if expired
    except Exception:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

    #fetch user by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(*role_names: str):
    """
    Returns a dependency that ensures current user has atleast one required roles
    """
    async def _checker(
            user: User = Depends(current_user),
            db: AsyncSession = Depends(get_session)
    )-> User:
        #Query roles names for this user

        q = await db.execute(
            select(Role.name)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == user.id)
        )

        user_roles = {row[0] for row in q.all()}        #set of roles names


        #if none of the required roles present show 403
        if not any(r in user_roles for r in role_names):
            raise HTTPException(status_code=403,detail="Forbidden")
        return user
    return _checker
