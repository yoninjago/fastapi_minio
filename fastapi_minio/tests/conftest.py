import pytest
from starlette.testclient import TestClient
from pathlib import Path
from ..database.models import MinioUploadedFiles
from .conf_test_db import app, override_get_session

REQUEST_CODE = 8
TEST_FILENAME = 'test.jpg'
IMG_FILE = Path('./tests/', 'image.jpg')
SMALL_IMAGE = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00'
        b'\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b')


@pytest.fixture()
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(autouse=True)
def create_database_obj(tmpdir):
    database = next(override_get_session())
    new_files_info = MinioUploadedFiles(request_code=REQUEST_CODE, filename=TEST_FILENAME)
    database.add(new_files_info)
    database.commit()
    yield


@pytest.fixture()
def create_image_file(tmpdir):
    with open(IMG_FILE, 'wb') as f:
        f.write(SMALL_IMAGE)
    yield
    IMG_FILE.unlink()
