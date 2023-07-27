from src.schemas import UserLoginSchema
from src.utils.crud import get_users
from sqlalchemy.orm import Session


async def check_user(data: UserLoginSchema, db: Session):
    users = await get_users(db)
    for user in users:
        if user[0].email == data.email and user[0].password == data.password:
            return True
    return False
