import sqlite3

NOM_FICHIER_SQL = 'bdd.sql'
NOM_FICHIER_BDD = 'base_de_donnees.db'

try:
    conn = sqlite3.connect(NOM_FICHIER_BDD)
    print(f"Connexion à la base de données '{NOM_FICHIER_BDD}' réussie.")

    with open(NOM_FICHIER_SQL, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    print(f"Script SQL '{NOM_FICHIER_SQL}' exécuté avec succès.")
    conn.commit()
except sqlite3.Error as e:
    print(f"Erreur lors de l'exécution du script SQL : {e}")
except FileNotFoundError:
    print(f"Le fichier SQL '{NOM_FICHIER_SQL}' est introuvable.")
finally:
    if conn:
        conn.close()
        print("Connexion à la base de données fermée.")