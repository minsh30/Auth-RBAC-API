#/api/auth.py

from fastapi import APIRouter, Depends, HTTPException 
from pydantic import BaseModel, EmailStr 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from app.db.session import get_session
from app.db.models import User, UserRole, Role
from app.core.security import hash_password, create_token, verify_password

#Group routes under /auth
router = APIRouter(prefix = "/auth", tags=["auth"])


#import model for registration
class RegisterIn(BaseModel):
    email:EmailStr
    password:str

@router.post("/register")
async def register(data: RegisterIn, db: AsyncSession = Depends(get_session)):
    """
    Creates a new user with default User role
    """

    #check if email already exists
    exists = (await db.execute(select(User).where(User.email==data.email))).scalar_one_or_none()
    if exists:
        raise HTTPException(400, "Email already exists!!")
    
    #create the user with hashed password
    user = User(email=data.email, hashed_password = hash_password(data.password))
    db.add(user)


    #Ensures a "user" role exists or create if missing
    role = (await db.execute(select(Role).where(Role.name == "user"))).scalar_one_or_none()
    if not role:
        role = Role(name="user")
        db.add(role)

    
    #Flush to assign IDS without commiting yet
    await db.flush()

    #Link the user to 'user role
    db.add(UserRole(user_id=user.id,role_id = role.id))

    #Persist changes
    await db.commit()
    return {"ok" : True}

#Input model for login
class LoginIn(BaseModel):
    email:EmailStr
    password:str

@router.post("/login")
async def login(data: LoginIn, db: AsyncSession = Depends(get_session)):
    """
    Verify credentials and returns a JWT access token
    """

    #Look up the user
    user = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()

    #Rejects if usermissing or password wrong
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401,"Invalid Credentials")
    
    #Create and return token
    token = create_token(user.email)
    return {"acces_token" : token, "token_type": "bearer"}

