import asyncio
from sqlalchemy import select
from app.db.session import engine, AsyncSessionLocal
from app.db.models import Base, User, Role, UserRole

EMAIL_TO_MAKE_ADMIN = "testadmin@gmail.com"  # <-- change to your email

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as s:
        user = (await s.execute(select(User).where(User.email == EMAIL_TO_MAKE_ADMIN))).scalar_one_or_none()
        if not user:
            print(f"User {EMAIL_TO_MAKE_ADMIN} not found. Register first.")
            return

        role = (await s.execute(select(Role).where(Role.name=="admin"))).scalar_one_or_none()
        if not role:
            role = Role(name="admin"); s.add(role); await s.flush()

        link = (await s.execute(
            select(UserRole).where(UserRole.user_id==user.id, UserRole.role_id==role.id)
        )).scalar_one_or_none()
        if not link:
            s.add(UserRole(user_id=user.id, role_id=role.id))

        await s.commit()
        print(f"Granted 'admin' to {EMAIL_TO_MAKE_ADMIN}")

asyncio.run(main())
