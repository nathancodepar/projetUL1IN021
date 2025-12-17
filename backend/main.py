import sqlite3
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. Configuration des dossiers (Pour que ça marche sur GitHub et en local)
base_dir = os.path.dirname(os.path.abspath(__file__))
dossier_frontend = os.path.join(base_dir, '..', 'frontend')
dossier_static = os.path.join(dossier_frontend, 'static')

# 2. On lie les fichiers CSS et HTML à l'appli
if os.path.exists(dossier_static):
    app.mount("/static", StaticFiles(directory=dossier_static), name="static")

templates = Jinja2Templates(directory=dossier_frontend)



# Vérification du respect des conditions
def verifier_conditions(user_id, temp_actuel, son_actuel, lum_actuelle):
    alertes = []
    
    # Chemin vers la base de données
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'database', 'base_de_donnees.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récup des préférences utilisateur
        cursor.execute("SELECT temperature, son, luminosite FROM preferences WHERE id = ?", (user_id,))
        tous_les_resultats = cursor.fetchall() 
        conn.close()
        
        # Si on a trouvé l'utilisateur, on vérifie les seuils
        if len(tous_les_resultats) > 0:
            resultat = tous_les_resultats[0]
            seuil_temp_max, seuil_son_max, seuil_lum_min = resultat
            
            # Tests des valeurs
            if temp_actuel > seuil_temp_max:
                alertes.append(f"ALERTE TEMPÉRATURE : {temp_actuel}°C (Max : {seuil_temp_max}°C)")
            if son_actuel > seuil_son_max:
                alertes.append(f"ALERTE SON : Niveau {son_actuel} (Max : {seuil_son_max})")
            if lum_actuelle < seuil_lum_min:
                alertes.append(f"ALERTE LUMINOSITÉ : Trop sombre ({lum_actuelle} < {seuil_lum_min})")
        
    except sqlite3.Error as error:
        print(f"Erreur connexion BDD : {error}")
        
    return alertes

# Modification des seuils (Quand l'utilisateur valide le formulaire)
def modifier_seuils(user_id, nouvelle_temp, nouveau_son, nouvelle_lum):
    # Chemin vers la BDD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'database', 'base_de_donnees.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Mise à jour des données
        query = "UPDATE preferences SET temperature = ?, son = ?, luminosite = ? WHERE id = ?"
        cursor.execute(query, (nouvelle_temp, nouveau_son, nouvelle_lum, user_id))
        
        # Validation
        conn.commit()
        conn.close()
        return "Réglages mis à jour avec succès."

    except sqlite3.Error as error:
        return f"Erreur lors de la modification : {error}"


# PARTIE SITE WEB

# Page d'accueil
@app.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    # REMPLACER VALEURS !!!!
    temp_actuelle = 22
    son_actuel = 40
    lum_actuelle = 600
    
    # On lance la vérification
    mes_alertes = verifier_conditions(1, temp_actuelle, son_actuel, lum_actuelle)
    
    # On envoie tout ça au fichier HTML
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "alertes": mes_alertes,
        "temp": temp_actuelle
    })

# Réception du formulaire de modification
@app.post("/modifier", response_class=HTMLResponse)
async def mise_a_jour(request: Request, temp: int = Form(...), son: int = Form(...), lum: int = Form(...)):
    
    # On appelle la fonction pour changer les réglages dans la BDD
    message = modifier_seuils(1, temp, son, lum)
    print(message) # Juste pour vérifier dans le terminal
    
    # On recharge la page avec le message de confirmation
    return templates.TemplateResponse("index.html", {
        "request": request,
        "info": message,
        "temp": 22, 
        "alertes": [] 
    })
"""
# PARTIE MINUTEUR !!!
@app.on_event("startup")
async def demarrer_minuteur():
    # Au lancement, on active la boucle de surveillance
    asyncio.create_task(boucle_de_surveillance())
"""
