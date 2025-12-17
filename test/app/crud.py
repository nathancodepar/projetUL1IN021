from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_last_measurement(db: Session):
    return db.query(models.Measurement).order_by(models.Measurement.id.desc()).first()

def create_measurement(db: Session, measurement: schemas.MeasurementBase, is_optimal: bool):
    db_meas = models.Measurement(**measurement.dict(), is_optimal=is_optimal)
    db.add(db_meas)
    db.commit()
    db.refresh(db_meas)
    return db_meas

def get_preferences(db: Session):
    prefs = db.query(models.Preference).first()
    if not prefs:
        prefs = models.Preference(id=1)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    return prefs

def update_preferences(db: Session, prefs: schemas.PreferenceBase):
    db_prefs = get_preferences(db)
    for var, value in vars(prefs).items():
        setattr(db_prefs, var, value)
    db.commit()
    db.refresh(db_prefs)
    return db_prefs