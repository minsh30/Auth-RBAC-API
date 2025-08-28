#/api/users.py

from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from pydantic import BaseModel, EmailStr 
from app.core.deps import current_user, require_role
from app.db.models import User, UserRole, Role
from app.db.session import get_session

router = APIRouter(prefix = "/users", tags=["users"])

@router.get("/me")
async def me(user = Depends(current_user)):
    """
    Return the profile of the currently authenticated user
    """

    return {"email" : user.email}

class RoleIn(BaseModel):
    email:EmailStr
    role: str

@router.post("/assign-role")            #RBAC: only admins are allowed.
async def assign_role(
    data: RoleIn,
    _admin = Depends(require_role("admin")),            #only admins can call this
    db: AsyncSession = Depends(get_session)
):
    """
    Grant a role to a user. Creates the role if doesn't exists
    """

    #find the target user

    u = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User Not Found")
    
    #Get or create role
    r = (await db.execute(select(Role).where(Role.name == data.role))).scalar_one_or_none()
    if not r:
        r = Role(name = data.role)
        db.add(r)
        await db.flush()

    # check if user already has this role
    existing = (await db.execute(
        select(UserRole).where(UserRole.user_id == u.id, UserRole.role_id == r.id)
    )).scalar_one_or_none()

    if not existing:
        db.add(UserRole(user_id=u.id, role_id=r.id))
    await db.commit()
    return{'ok' : True}



