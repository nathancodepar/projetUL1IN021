document.getElementById('conditionsForm').addEventListener('submit', function(event) {
    // Empêche le rechargement de la page par défaut du formulaire
    event.preventDefault();

    // 1. Récupération des valeurs
    const conditions = {
        temperature: {
            min: parseFloat(document.getElementById('tempMin').value),
            max: parseFloat(document.getElementById('tempMax').value)
        },
        sound: {
            min: parseFloat(document.getElementById('soundMin').value),
            max: parseFloat(document.getElementById('soundMax').value)
        },
        light: {
            min: parseFloat(document.getElementById('lightMin').value),
            max: parseFloat(document.getElementById('lightMax').value)
        }
    };

    // 2. Affichage des valeurs (Simule l'envoi à la Raspberry Pi)
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <h3>✅ Conditions Prêtes à être Envoyées :</h3>
        <p>Le JSON ci-dessous serait envoyé à l'API de la Raspberry Pi :</p>
        <pre>${JSON.stringify(conditions, null, 2)}</pre>
    `;

    // 3. Étape d'implémentation future : Envoyer les données à la Raspberry Pi (RPi)
    // Pour que la RPi reçoive ces données, vous devrez implémenter un serveur
    // sur la RPi (par exemple, avec Flask en Python) qui écoutera les requêtes POST.

    /*
    fetch('http://ADRESSE_IP_DE_VOTRE_RASPBERRY_PI/set_conditions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(conditions),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Succès:', data);
        resultDiv.innerHTML = `Conditions envoyées avec succès à la RPi !`;
    })
    .catch((error) => {
        console.error('Erreur lors de l\'envoi:', error);
        resultDiv.innerHTML = 'Erreur lors de la connexion à la RPi.';
    });
    */
});