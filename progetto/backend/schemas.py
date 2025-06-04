from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    confirm_password: str


class UserProfileCreate(BaseModel):
    indirizzo: str
    citta: str
    cap: str
    telefono: str
    zona_operativa: Optional[str] = None
    raggio_km: Optional[int] = None
    veicolo: Optional[str] = None
    patente: Optional[str] = None
    partita_iva: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class TokenData(BaseModel):
    email: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: int
    user_id: int
    indirizzo: str
    citta: str
    cap: str
    telefono: str
    zona_operativa: Optional[str]
    raggio_km: Optional[int]
    veicolo: Optional[str]
    patente: Optional[str]
    partita_iva: Optional[str]
    rating_medio: float

    class Config:
        from_attributes = True


class UserDetail(User):
    profile: UserProfile

    class Config:
        from_attributes = True 