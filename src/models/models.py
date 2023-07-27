from sqlalchemy import Boolean, Column, Integer, String, Text, UUID, DateTime, func
import uuid
from src.db.database import Base


class USER(Base):
    __tablename__ = "users"

    if 'users' not in Base.metadata.tables:
        id = Column(Integer, primary_key=True)
        fullname = Column(Text, unique=True, index=True)
        email = Column(Text, unique=True, index=True)
        password = Column(Text, index=True)
        created_at = Column(DateTime, server_default=func.now())


class Files(Base):
    __tablename__ = "downloads_files"

    if 'dowloads_files' not in Base.metadata.tables:
        id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
        name = Column(String(50), index=True)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now())
        path = Column(String(100), nullable=False)
        size = Column(Integer, nullable=False)
        is_downloadable = Column(Boolean, default=True)
