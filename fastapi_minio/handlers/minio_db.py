from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import models
from ..database.database import get_session


class MinioDbHandler():
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_list(self, request_code: int) -> list[models.MinioUploadedFiles]:
        files_objs = (
            self.session.query(models.MinioUploadedFiles)
            .filter_by(request_code=request_code)
            .all())
        if not files_objs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return files_objs

    def get_list(self, request_code: int) -> list[models.MinioUploadedFiles]:
        return self._get_list(request_code)

    def create(
            self,
            filename: str,
            request_code: int) -> models.MinioUploadedFiles:
        insert_object = models.MinioUploadedFiles(
            filename=filename, request_code=request_code)
        self.session.add(insert_object)
        self.session.commit()
        return insert_object

    def get_new_request_code(self):
        obj_last_request_code = (
            self.session.query(models.MinioUploadedFiles)
            .order_by(models.MinioUploadedFiles.request_code.desc())
            .first())
        if not obj_last_request_code:
            return 1
        return obj_last_request_code.request_code + 1

    def delete(self, request_code: int) -> dict:
        objs = self._get_list(request_code)
        files_names = []
        for obj in objs:
            files_names.append(obj.filename)
            self.session.delete(obj)
        self.session.commit()
        return {
            'files_names': files_names,
            'create_date': objs[0].created_at.strftime('%Y%m%d')}
