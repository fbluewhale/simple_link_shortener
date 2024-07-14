from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


class LogBase(BaseModel):
    application_ip: str
    browser: str
    channel: str = "middleware"
    client_ip: str
    device: str = "Other"
    duration: Optional[float]
    extra_fields: Optional[Dict[str, Any]] = None
    operation_name: str = "forward_request"
    os: str = "Other"
    req_data: Dict[str, Any]
    req_method: str
    req_time: datetime
    req_url: str
    res_data: Optional[Dict[str, Any]]
    res_status_code: Optional[int]
    res_time: Optional[datetime]
    tracking_number: Optional[str]
    user_id: str
    username: str


class RequestLog(BaseModel):
    req_method: str
    req_url: str
    req_time: datetime = Field(default_factory=lambda: datetime.now())
    req_data: Dict[str, Any] = {}
    client_ip: str
    user_id: Optional[str]
    username: Optional[str]


class ResponseLog(BaseModel):
    res_status_code: int
    res_time: datetime = Field(default_factory=datetime.now)
    res_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    duration: float
