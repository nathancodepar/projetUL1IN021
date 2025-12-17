from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from datetime import datetime
from .database import Base

class Measurement(Base):
    """
    Modèle pour stocker les mesures des capteurs.
    """
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)  # Température en degrés Celsius
    luminosity = Column(Float)   # Luminosité (valeur brute ou Lux)
    sound_level = Column(Float)  # Niveau sonore (valeur brute ou dB)
    is_optimal = Column(Boolean) # Vrai si les conditions sont dans l'intervalle de préférence

class Preference(Base):
    """
    Modèle pour stocker les préférences de l'utilisateur.
    """
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True) # Une seule ligne sera utilisée (id=1)
    min_temp = Column(Float, default=20.0)
    max_temp = Column(Float, default=24.0)
    min_lumi = Column(Float, default=50.0)
    max_lumi = Column(Float, default=500.0)
    min_sound = Column(Float, default=30.0)
    max_sound = Column(Float, default=60.0)