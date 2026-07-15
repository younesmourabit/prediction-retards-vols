document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(e) {
        e.preventDefault(); // Empêche la soumission normale du formulaire

        // Afficher le chargement
        resultDiv.innerHTML = "Prédiction en cours...";
        resultDiv.style.backgroundColor = "#333";
        resultDiv.style.color = "white";
        resultDiv.style.padding = "20px";

        // Récupérer les données du formulaire
        const formData = new FormData(form);
        const data = {
            DAY: parseInt(formData.get('DAY')),
            MONTH: parseInt(formData.get('MONTH')),
            YEAR: parseInt(formData.get('YEAR')),
            DISTANCE: parseFloat(formData.get('DISTANCE')),
            CRS_DEP_TIME: formData.get('CRS_DEP_TIME'),
            DEP_TIME: formData.get('DEP_TIME'),
            CRS_ARR_TIME: formData.get('CRS_ARR_TIME'),
            ORIGIN: formData.get('ORIGIN').toUpperCase(),
            AIRLINE: formData.get('AIRLINE').trim().toUpperCase(), // Conversion en majuscules
            DEST: formData.get('DEST').toUpperCase()
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Formater le résultat
            resultDiv.style.whiteSpace = 'pre-line';
            resultDiv.style.fontFamily = 'monospace';
            
            if (result.error) {
                resultDiv.style.backgroundColor = "#dc3545";
                resultDiv.textContent = `Erreur: ${result.error}`;
                return;
            }

            if (result.retard) {
                resultDiv.style.backgroundColor = "#dc3545";
                resultDiv.textContent = `Bienvenue dans le menu de prédiction des retards de vol !

Retard : Oui
Durée du retard : ${result.duree} minutes
Cause du retard : ${result.cause}`;
            } else {
                resultDiv.style.backgroundColor = "#28a745";
                resultDiv.textContent = `Bienvenue dans le menu de prédiction des retards de vol !

Retard : Non`;
            }

        } catch (error) {
            console.error('Erreur:', error);
            resultDiv.style.backgroundColor = "#dc3545";
            resultDiv.textContent = "Erreur lors de la prédiction";
        }
    });
});