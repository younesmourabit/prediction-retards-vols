document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Simulation simple (à remplacer avec fetch vers ton backend Flask)
    const delay = Math.floor(Math.random() * 40); // aléatoire entre 0 et 40

    const resultDiv = document.getElementById('result');
    if (delay > 15) {
        resultDiv.textContent = `❌ Votre vol risque d’avoir un retard de ${delay} minutes.`;
        resultDiv.style.backgroundColor = "rgba(255, 0, 0, 0.6)";
    } else {
        resultDiv.textContent = `✅ Pas de retard significatif prévu (${delay} min).`;
        resultDiv.style.backgroundColor = "rgba(0, 128, 0, 0.6)";
    }
});
