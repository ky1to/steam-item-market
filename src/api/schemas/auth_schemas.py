from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SAuthUser(BaseModel):
    name: str
    password: str

class SUser(BaseModel):
    name: str
    hash_password: str
    model_config = ConfigDict(strict=True, from_attributes=True)

class SNewUser(SUser):
    email: str

class SAuth(SNewUser):
    role: str

class SToken(BaseModel):
    access_token: str