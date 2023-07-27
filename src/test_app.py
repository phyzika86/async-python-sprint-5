"""
test_upload не проходит, не могу разобраться почему. В /upload вызывается crud.upload_file
В котором не отрабатывает row = (await db.execute(statement)).first()
Хотя test_create_user также есть обращение к БД, в котором запрос выполняется успешно...
"""

from fastapi.testclient import TestClient
from utils import session_utils
import random
import string
from src.auth.auth_handler import signJWT
import psycopg2
from psycopg2.extras import NamedTupleCursor

from main import app

client = TestClient(app)
get_session = session_utils.get_session


def test_read_root():
    response = client.get('/api/v1')
    assert response.status_code == 200
    assert response.json() == "Добро пожаловать в Файловое хранилище"


def test_create_user():
    letters = string.ascii_lowercase
    test_user = {
        "fullname": ''.join(random.choice(letters) for _ in range(10)),
        "email": ''.join(random.choice(letters) for _ in range(10)),
        "password": ''.join(random.choice(letters) for _ in range(10))
    }
    response = client.post('/api/v1/register', json=test_user)
    jwt = signJWT(test_user.get('email'))
    assert response.status_code == 200
    result = response.json()
    assert 'access_token' in result
    assert len(jwt['access_token']) == len(result['access_token'])


def test_register():
    letters = string.ascii_lowercase
    test_user = {
        "fullname": ''.join(random.choice(letters) for _ in range(10)),
        "email": ''.join(random.choice(letters) for _ in range(10)),
        "password": ''.join(random.choice(letters) for _ in range(10))
    }
    response = client.post('/api/v1/register', json=test_user)
    conn = psycopg2.connect(dbname='collection', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor = conn.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute('select * from users order by created_at desc')
    res = cursor.fetchall()[0]
    assert res.fullname == test_user['fullname']
    assert res.email == test_user['email']
    assert res.password == test_user['password']
    conn.close()


def test_upload():
    letters = string.ascii_lowercase
    test_user = {
        "fullname": ''.join(random.choice(letters) for _ in range(10)),
        "email": ''.join(random.choice(letters) for _ in range(10)),
        "password": ''.join(random.choice(letters) for _ in range(10))
    }
    response = client.post('/api/v1/register', json=test_user)
    result = response.json()
    token = result['access_token']
    response = client.post('/api/v1/upload', headers={'authorization': f'Bearer {token}'},
                           params={'path': '/file/test/'}, files={'file': open('test.txt', 'rb')})


def test_autorization():
    letters = string.ascii_lowercase
    test_user = {
        "fullname": ''.join(random.choice(letters) for _ in range(10)),
        "email": ''.join(random.choice(letters) for _ in range(10)),
        "password": ''.join(random.choice(letters) for _ in range(10))
    }
    response = client.post('/api/v1/register', json=test_user)
    result = response.json()
    token = result['access_token']
    response = client.post('/api/v1/test_autorization', headers={'authorization': f'Bearer {token}'},
                           params={'msg': 'test'})
    result = response.json()
    assert result == 'autorization_success'
