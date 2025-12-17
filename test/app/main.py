import threading
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .sensors import reader

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def background_task():
    while True:
        db = next(database.get_db())
        prefs = crud.get_preferences(db)
        t, l, s = reader.read_temperature(), reader.read_luminosity(), reader.read_sound_level()
        
        is_opti = (prefs.min_temp <= t <= prefs.max_temp and 
                   prefs.min_lumi <= l <= prefs.max_lumi and 
                   prefs.min_sound <= s <= prefs.max_sound)
        
        crud.create_measurement(db, schemas.MeasurementBase(temperature=t, luminosity=l, sound_level=s), is_opti)
        threading.Event().wait(30)

@app.on_event("startup")
def startup():
    threading.Thread(target=background_task, daemon=True).start()

@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "last": crud.get_last_measurement(db),
        "prefs": crud.get_preferences(db)
    })

@app.post("/update_prefs")
def update_prefs(min_t: float=Form(...), max_t: float=Form(...), min_l: float=Form(...), 
                 max_l: float=Form(...), min_s: float=Form(...), max_s: float=Form(...), 
                 db: Session = Depends(database.get_db)):
    new_p = schemas.PreferenceBase(min_temp=min_t, max_temp=max_t, min_lumi=min_l, max_lumi=max_l, min_sound=min_s, max_sound=max_s)
    crud.update_preferences(db, new_p)
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/calibrate")
def calibrate():
    return {"t": reader.read_temperature(), "l": reader.read_luminosity(), "s": reader.read_sound_level()}