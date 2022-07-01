from datetime import datetime

from pydantic import BaseModel


class MinioFilesBased(BaseModel):
    filename: str

    class Config:
        orm_mode = True


class MinioUploadedFiles(MinioFilesBased):
    created_at: datetime
