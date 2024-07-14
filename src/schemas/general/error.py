from pydantic import BaseModel, Field
from typing import Optional, Union, List

from src.models.base import BaseDocument


class BaseErrorInstance(BaseModel):
    msg_fa: str | None = None
    msg: str | None = None


class BaseError(BaseModel):
    detail: BaseErrorInstance


class UploadFileErrorInstance(BaseErrorInstance):
    type: str | None = None
    error_file_path: str | None = None
    loc: Optional[Union[List[Union[str, Union[int, str]]], str]] = None


class UploadFileError(BaseModel):
    detail: UploadFileErrorInstance
