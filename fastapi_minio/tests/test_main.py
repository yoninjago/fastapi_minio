from datetime import datetime

from ..database.models import MinioUploadedFiles
from .conf_test_db import override_get_session
from .conftest import IMG_FILE, REQUEST_CODE, TEST_FILENAME, test_app

NEXT_REQUEST_CODE = REQUEST_CODE + 1
FRAMES_URL = '/frames/' + str(REQUEST_CODE)


def test_get(test_app):
    response = test_app.get(FRAMES_URL)
    assert response.status_code == 200
    assert response.json() == [{
        'filename': TEST_FILENAME,
        'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")}]


def test_delete(test_app):
    response = test_app.delete(FRAMES_URL)
    db_objs = (
        next(override_get_session())
        .query(MinioUploadedFiles)
        .filter_by(request_code=REQUEST_CODE)
        .all())
    assert db_objs == []
    assert response.status_code == 204


def test_post(test_app, create_image_file):
    response = test_app.post(
        '/frames/',
        files={'files': ('filename', open(IMG_FILE, 'rb'), 'image/jpeg')})
    filename = (
        next(override_get_session())
        .query(MinioUploadedFiles)
        .filter_by(request_code=NEXT_REQUEST_CODE)
        .all()[0].filename)
    assert response.status_code == 201
    assert response.json() == [{"filename": filename}]
