from pydantic import BaseModel, HttpUrl
from typing import Optional

class CompanySettingsBase(BaseModel):
    company_name: Optional[str] = None
    primary_color: Optional[str] = None

class CompanySettingsUpdate(CompanySettingsBase):
    pass

class CompanySettings(CompanySettingsBase):
    id: int
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True