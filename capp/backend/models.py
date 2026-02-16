from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class PredictionResult(BaseModel):
    filename: str
    object_count: int
    details: Dict[str, int]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
