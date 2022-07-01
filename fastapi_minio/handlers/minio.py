import uuid
from datetime import datetime
from io import BytesIO

from minio import Minio

from ..settings import settings


class MinioHandler():
    __instance = None

    @staticmethod
    def get_instance():
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance

    def __init__(self):
        self.minio_url = settings.minio_url
        self.access_key = settings.minio_access_key
        self.secret_key = settings.minio_secret_key
        self.bucket_name = datetime.now().strftime('%Y%m%d')
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )
        self.make_bucket()

    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def put_object(self, file_data: BytesIO, content_type: str) -> str:
        object_name = f'{str(uuid.uuid4())}.jpg'
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=file_data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        return object_name

    def delete_object(self, files_info: dict):
        for filename in files_info['files_names']:
            self.client.remove_object(
                bucket_name=files_info['create_date'],
                object_name=filename
            )
