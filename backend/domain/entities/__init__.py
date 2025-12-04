from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Entity(BaseModel):
    """Base domain entity"""
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
