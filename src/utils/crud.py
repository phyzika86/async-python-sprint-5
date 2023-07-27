from sqlalchemy.orm import Session
from sqlalchemy import select, update, func, and_
from fastapi import Depends, UploadFile
from src.utils import session_utils
from src.models import models
import src.schemas as schemas
from sqlalchemy import and_
from decouple import config

User = models.USER

get_session = session_utils.get_session


async def create_user(user: schemas.UserSchema, db: Session = Depends(get_session)) -> User:
    user = User(
        fullname=user.fullname, email=user.email, password=user.password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_users(db: Session = Depends(get_session)):
    statement = select(models.USER)
    rows = (await db.execute(statement)).fetchall()
    return rows


async def upload_file(file_name: str, path: str, size, db: Session = Depends(get_session)):
    path = f'/{config("DOWNLOAD_DIR")}{path}'
    file = models.Files(
        name=file_name, path=path, size=size
    )
    statement = select(models.Files).where(and_(models.Files.path == path, models.Files.name == file_name))
    row = (await db.execute(statement)).first()
    if not row:
        db.add(file)
    else:
        stmt = update(models.Files).where(models.Files.id == row[0].id).values(size=size, updated_at=func.now())
        await db.execute(statement=stmt)
        file = (await db.execute(statement)).first()[0]

    await db.commit()

    return file


async def get_file_by_id(id: str, db: Session = Depends(get_session)):
    statement = select(models.Files).where(models.Files.id == id)
    row = (await db.execute(statement)).first()
    return row[0]


async def get_files(db: Session = Depends(get_session)):
    statement = select(models.Files)
    row = (await db.execute(statement)).scalars().all()
    return row
