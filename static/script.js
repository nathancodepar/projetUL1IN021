// Éléments du DOM
const statusBox = document.getElementById('status-box');
const showTipsCheckbox = document.getElementById('show-tips');
const tipsBox = document.getElementById('tips-box');
const monitorMsg = document.getElementById('monitor-msg');

/**
 * Mise à jour des données capteurs
 */
async function updateData() {
    try {
        const response = await fetch('/api/current');
        const data = await response.json();
        
        if (data.temp !== undefined) {
            document.getElementById('temp-val').innerText = `${data.temp} °C`;
            document.getElementById('light-val').innerText = `${data.light} lx`;
            document.getElementById('sound-val').innerText = `${data.sound} dB`;
            
            statusBox.innerText = `ÉTAT ACTUEL : ${data.status}`;
            statusBox.style.backgroundColor = (data.status === "IDÉAL") ? "#27ae60" : "#e74c3c";
        }
    } catch (e) {
        console.error("Erreur lecture API", e);
    }
}

/**
 * Gestion du moniteur (Démarrer/Arrêter)
 */
async function controlMonitor(action) {
    try {
        const response = await fetch(`/api/monitor/${action}`, { method: 'POST' });
        const data = await response.json();
        monitorMsg.innerText = data.status;
        checkMonitorStatus();
    } catch (e) {
        console.error("Erreur contrôle moniteur", e);
    }
}

async function checkMonitorStatus() {
    try {
        const response = await fetch('/api/monitor/status');
        const data = await response.json();
        const startBtn = document.getElementById('btn-start');
        const stopBtn = document.getElementById('btn-stop');

        if (data.running) {
            startBtn.disabled = true; startBtn.style.opacity = "0.5";
            stopBtn.disabled = false; stopBtn.style.opacity = "1";
            monitorMsg.innerText = "Le moniteur est en cours d'exécution";
            monitorMsg.style.color = "#27ae60";
        } else {
            startBtn.disabled = false; startBtn.style.opacity = "1";
            stopBtn.disabled = true; stopBtn.style.opacity = "0.5";
            monitorMsg.innerText = "Le moniteur est arrêté";
            monitorMsg.style.color = "#e74c3c";
        }
    } catch (e) { console.log("Serveur non prêt"); }
}

/**
 * Préférences
 */
async function loadPreferences() {
    try {
        const response = await fetch('/api/preferences');
        const prefs = await response.json();
        document.getElementById('min_temp').value = prefs.min_temp;
        document.getElementById('max_temp').value = prefs.max_temp;
        document.getElementById('min_light').value = prefs.min_light;
        document.getElementById('min_sound').value = prefs.min_sound;
    } catch (e) { console.error("Erreur chargement prefs", e); }
}

async function savePreferences() {
    const prefs = {
        min_temp: parseFloat(document.getElementById('min_temp').value),
        max_temp: parseFloat(document.getElementById('max_temp').value),
        min_light: parseFloat(document.getElementById('min_light').value),
        min_sound: parseFloat(document.getElementById('min_sound').value)
    };

    const response = await fetch('/api/preferences', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(prefs)
    });

    if (response.ok) alert("Réglages enregistrés !");
}

/**
 * Recommandations
 */
showTipsCheckbox.addEventListener('change', function() {
    tipsBox.style.display = this.checked ? 'block' : 'none';
});

function applyDefaults() {
    document.getElementById('min_temp').value = 19.0;
    document.getElementById('max_temp').value = 24.0;
    document.getElementById('min_light').value = 300;
    document.getElementById('min_sound').value = 60;
}

// Initialisation
loadPreferences();
checkMonitorStatus();
setInterval(updateData, 5000); // Mise à jour toutes les 5 secondes
updateData();