import pandas as pd
from ydata_profiling import ProfileReport

# 1. Charger le CSV
dataclean = pd.read_csv("dataclean.csv")

# 2. Créer le rapport
profile = ProfileReport(
    dataclean,
    title="Flight Delay Data Profiling Report",
    explorative=True
)

# 3. Exporter le rapport HTML
profile.to_file("flight_delay_profiling_report.html")

print("Rapport généré avec succès !")
