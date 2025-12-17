from pydantic import BaseModel
from datetime import datetime

class MeasurementBase(BaseModel):
    temperature: float
    luminosity: float
    sound_level: float

class MeasurementCreate(MeasurementBase):
    pass

class Measurement(MeasurementBase):
    id: int
    timestamp: datetime
    is_optimal: bool
    class Config:
        from_attributes = True

class PreferenceBase(BaseModel):
    min_temp: float
    max_temp: float
    min_lumi: float
    max_lumi: float
    min_sound: float
    max_sound: float

class Preference(PreferenceBase):
    id: int
    class Config:
        from_attributes = True