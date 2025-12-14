import sqlite3
import os

# Vérification du respect des conditions 
def verifier_conditions(user_id, temp_actuelle, son_actuel, lum_actuelle):
    alertes = []
    
    # Chemin vers la base de données
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'database', 'base_de_donnees.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récup des préférences
        cursor.execute("SELECT temperature, son, luminosite FROM preferences WHERE id = ?", (user_id,))
        
        tous_les_resultats = cursor.fetchall() 
        conn.close()
        
        # Si la liste n'est pas vide (si on a trouvé l'utilisateur)
        if len(tous_les_resultats) > 0:
            # On prend la première ligne de la liste
            resultat = tous_les_resultats[0]
            
            seuil_temp_max, seuil_son_max, seuil_lum_min = resultat
            
            # Vérification des seuils 
            
            # Température
            if temp_actuelle > seuil_temp_max:
                alertes.append(f"ALERTE TEMPÉRATURE : {temp_actuelle}°C mesurés (Max : {seuil_temp_max}°C)")
                
            # Son
            if son_actuel > seuil_son_max:
                alertes.append(f"ALERTE SON : Niveau {son_actuel} trop élevé (Max : {seuil_son_max})")
                
            # Luminosité
            if lum_actuelle < seuil_lum_min:
                alertes.append(f"ALERTE LUMINOSITÉ : Trop sombre ({lum_actuelle} < {seuil_lum_min})")
        
    except sqlite3.Error as error:
        print(f"Erreur de connexion à la base de données : {error}")

    return alertes
