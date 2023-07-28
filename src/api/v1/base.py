from fastapi import HTTPException, Depends, APIRouter, UploadFile, Request
from fastapi.responses import FileResponse

from src.schemas import UserSchema, UserLoginSchema, FileSchema, DownloadFileSchema

from src.core.config import get_settings
from os import makedirs
from sqlalchemy.orm import Session
from src.utils import crud, session_utils
from src.utils.utils import check_user

from src.auth.auth_handler import signJWT
from src.auth.auth_bearer import JWTBearer
from decouple import config
from sqlalchemy.sql import text

router = APIRouter()

app_settings = get_settings()
get_session = session_utils.get_session


async def raise_error(message, status_code):
    raise HTTPException(status_code=status_code, detail=message)


@router.get("/", description="Стартовая страница файлового хранилища")
async def read_root():
    return "Добро пожаловать в Файловое хранилище"


@router.get('/ping', description="Статус активности связанных сервисов")
async def get_ping(db: Session = Depends(get_session)):
    try:
        await db.execute(text("SELECT pg_database_size('collection') database_size"))
        res = 'Подключение к БД выполнено успешно'
    except Exception as e:
        res = f'Возникли проблемы с подключением к БД {e}'
    return res


@router.post("/register", description="Зарегистрироваться")
async def create_user(user: UserSchema, db: Session = Depends(get_session)):
    await crud.create_user(db=db, user=user)
    return signJWT(user.email)


@router.post("/login", description="Залогиниться")
async def user_login(user: UserLoginSchema, db: Session = Depends(get_session)):
    if await check_user(user, db=db):
        return signJWT(user.email)

    await raise_error("не найден login", 404)


@router.post("/upload", description="Загрузка файлов", response_model=FileSchema)
async def upload_file(request: Request, file: UploadFile, path: str, db: Session = Depends(get_session)):
    file_name = file.filename
    file_extension = file_name.split('.')[-1]
    split_path = path.split('/')
    is_file_name_in_path = '.' in split_path[-1]

    if is_file_name_in_path:
        file_name_from_path = split_path[-1].split('.')
        file_name_from_path[-1] = file_extension
        file_name = '.'.join(file_name_from_path)
        full_path = '/'.join(split_path[0:len(split_path) - 1]) + '/'
    else:
        full_path = path
    try:
        file_db = await crud.upload_file(file_name=file_name, path=full_path, size=file.size, db=db)
        response = FileSchema(
            id=file_db.id,
            name=file_db.name,
            created_at=str(file_db.created_at),
            updated_at=str(file_db.updated_at),
            path=file_db.path,
            size=file_db.size,
            is_downloadable=file_db.is_downloadable
        )
        full_path = f'./{config("DOWNLOAD_DIR")}{full_path}'
        makedirs(full_path, exist_ok=True)
        with open(f'{full_path}{file_name}', 'wb') as f:
            f.write(file.file.read())
    except Exception as e:
        response = FileSchema()

    return response


@router.post("/file/download", description="Скачать файл", dependencies=[Depends(JWTBearer())])
async def download_file(path: DownloadFileSchema, db: Session = Depends(get_session)):
    if path.id:
        file_info = await crud.get_file_by_id(id=path.id, db=db)
        full_path = f'.{file_info.path}{file_info.name}'
    else:
        full_path = path.path

    return FileResponse(path=full_path, filename='Статистика покупок.xlsx', media_type='multipart/form-data')


@router.get("/files", dependencies=[Depends(JWTBearer())])
async def get_files(db: Session = Depends(get_session)):
    files = await crud.get_files(db=db)
    return files


@router.post("/test_autorization", dependencies=[Depends(JWTBearer())], description="Тест аутентификации по токену")
async def autorization():
    return 'autorization_success'
