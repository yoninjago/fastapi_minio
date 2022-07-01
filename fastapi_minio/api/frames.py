from io import BytesIO

from fastapi import (
    APIRouter, Depends, File, Response, UploadFile, status, HTTPException)

from ..handlers.minio import MinioHandler
from ..handlers.minio_db import MinioDbHandler
from ..schemas.minio import MinioFilesBased, MinioUploadedFiles

router = APIRouter(
    prefix='/frames'
)


@router.post(
    '/',
    response_model=list[MinioFilesBased],
    status_code=201,
    tags=['minio'])
def upload_files_to_minio(
        files: list[UploadFile] = File(...),
        handler: MinioDbHandler = Depends()):
    if len(files) > 15:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail='Max 15 files allowed to upload')
    files_names = []
    request_code = handler.get_new_request_code()
    for file in files:
        data_file = MinioHandler().get_instance().put_object(
            file_data=BytesIO(file.file.read()),
            content_type=file.content_type)
        files_names.append(
            handler.create(filename=data_file, request_code=request_code))
    return files_names


@router.get(
    '/{request_code}',
    response_model=list[MinioUploadedFiles],
    tags=['minio'])
def get_uploaded_files_info(
        request_code: int,
        handler: MinioDbHandler = Depends()):
    return handler.get_list(request_code)


@router.delete('/{request_code}', tags=['minio'])
def delete_files_from_minio(
        request_code: int,
        handler: MinioDbHandler = Depends()):
    files_info = handler.delete(request_code)
    MinioHandler().get_instance().delete_object(files_info)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
