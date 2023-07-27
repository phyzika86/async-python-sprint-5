from pydantic import BaseModel
import uuid


class UserSchema(BaseModel):
    fullname: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Ivanov Petr Alexandrovich",
                "email": "ivanov@yandex.ru",
                "password": "weakpassword123@"
            }
        }


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@yandex.ru",
                "password": "weakpassword123@"
            }
        }


class FileSchema(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    name: str = "error.txt"
    created_at: str = "error"
    updated_at: str = "error"
    path: str = "error"
    size: int = -1
    is_downloadable: bool = False

    class Config:
        schema_extra = {
            "example": {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "name": "notes.txt",
                "created_ad": "2020-09-11T17:22:05Z",
                "updated_at": "",
                "path": "/homework/test-fodler/notes.txt",
                "size": 8512,
                "is_downloadable": True
            }
        }


class DownloadFileSchema(BaseModel):
    id: str = ''
    path: str = './download/default.txt'

    class Config:
        schema_extra = {
            "example": {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "path": "/homework/test-fodler/notes.txt",
            }
        }