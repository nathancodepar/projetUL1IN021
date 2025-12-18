// Constantes pour les éléments du DOM
const tempDisplay = document.getElementById('temp-val');
const lightDisplay = document.getElementById('light-val');
const soundDisplay = document.getElementById('sound-val');
const statusBox = document.getElementById('status-box');
const saveBtn = document.getElementById('btn-save');

/**
 * Récupère les dernières mesures du Raspberry Pi
 */
async function updateData() {
    try {
        const response = await fetch('/api/current');
        const data = await response.json();
        
        if (data.temp !== undefined) {
            // Mise à jour des textes
            tempDisplay.innerText = `${data.temp} °C`;
            lightDisplay.innerText = data.light;
            soundDisplay.innerText = data.sound;
            
            // Mise à jour de la bannière d'état
            statusBox.innerText = `ÉTAT ACTUEL : ${data.status}`;
            statusBox.style.backgroundColor = (data.status === "IDÉAL") ? "#27ae60" : "#e74c3c";
        }
    } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
        statusBox.innerText = "ERREUR DE CONNEXION AU SERVEUR";
        statusBox.style.backgroundColor = "#c0392b";
    }
}

/**
 * Charge les préférences enregistrées dans la base de données
 */
async function loadPreferences() {
    try {
        const response = await fetch('/api/preferences');
        const prefs = await response.json();
        
        document.getElementById('min_temp').value = prefs.min_temp;
        document.getElementById('max_temp').value = prefs.max_temp;
        document.getElementById('min_light').value = prefs.min_light;
        document.getElementById('min_sound').value = prefs.min_sound;
    } catch (error) {
        console.error("Erreur lors du chargement des préférences :", error);
    }
}

/**
 * Envoie les nouvelles préférences au serveur
 */
async function savePreferences() {
    const prefs = {
        min_temp: parseFloat(document.getElementById('min_temp').value),
        max_temp: parseFloat(document.getElementById('max_temp').value),
        min_light: parseFloat(document.getElementById('min_light').value),
        min_sound: parseFloat(document.getElementById('min_sound').value)
    };

    try {
        const response = await fetch('/api/preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(prefs)
        });

        if (response.ok) {
            alert("✅ Préférences enregistrées avec succès !");
            updateData(); // Rafraîchir l'affichage immédiatement
        } else {
            alert("❌ Erreur lors de l'enregistrement.");
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
    }
}

// Écouteur d'événement sur le bouton
saveBtn.addEventListener('click', savePreferences);

// Initialisation
loadPreferences(); // Charger les réglages au début
updateData();      // Première lecture des capteurs
setInterval(updateData, 10000); // Mise à jour automatique toutes les 10 secondes