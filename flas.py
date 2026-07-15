from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Définir les chemins absolus vers les modèles
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
CLF_PATH = os.path.join(MODEL_DIR, 'pipeline_clf.pkl')
REG_PATH = os.path.join(MODEL_DIR, 'pipeline_reg.pkl')
CAUSE_PATH = os.path.join(MODEL_DIR, 'pipeline_cause.pkl')

# Charger les modèles une seule fois au démarrage
try:
    print(f"Chargement des modèles depuis {MODEL_DIR}")
    pipeline_clf = joblib.load(CLF_PATH)
    pipeline_reg = joblib.load(REG_PATH)
    pipeline_cause = joblib.load(CAUSE_PATH)
    print("Modèles chargés avec succès")
except Exception as e:
    print(f"Erreur lors du chargement des modèles: {str(e)}")
    raise

# Liste des causes possibles
CAUSES = ["Problème compagnie", "Météo", "Trafic aérien", "Retour au hangar", "Autre"]

def time_to_minutes(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except Exception as e:
        raise ValueError(f"Format d'heure invalide ({time_str}). Utilisez HH:MM")

def custom_target_encoder(df, col):
    if col in df.columns:
        mean = df.groupby(col).size().to_dict()
        df[f"{col}_ENCODED"] = df[col].map(mean)
        df = df.drop(columns=[col])
    return df

def predire_retard(nouveau_vol):
    try:
        # Créer le DataFrame et encoder les variables
        df_nouveau_vol = pd.DataFrame([nouveau_vol])
        print("DataFrame initial:", df_nouveau_vol.columns)  # Debug

        df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'AIRLINE')
        df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'ORIGIN')
        df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'DEST')

        print("DataFrame encodé:", df_nouveau_vol.columns)  # Debug

        # Prédiction avec les modèles globaux
        retard_pred = pipeline_clf.predict(df_nouveau_vol)[0]
        print(f"Prédiction retard: {retard_pred}")  # Debug

        if retard_pred == 1:
            duree_retard_pred = pipeline_reg.predict(df_nouveau_vol)[0]
            cause_retard_pred = pipeline_cause.predict(df_nouveau_vol)[0]
            print(f"Durée: {duree_retard_pred}, Cause: {cause_retard_pred}")  # Debug
            return True, duree_retard_pred, cause_retard_pred
        else:
            return False, None, None

    except Exception as e:
        print(f"Erreur dans predire_retard: {str(e)}")  # Debug
        raise

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer et valider les données
        data = request.get_json()
        print("Données reçues:", data)  # Debug

        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400

        # Convertir les heures en minutes
        try:
            crs_dep_time_min = time_to_minutes(data['CRS_DEP_TIME'])
            dep_time_min = time_to_minutes(data['DEP_TIME'])
            crs_arr_time_min = time_to_minutes(data['CRS_ARR_TIME'])
        except ValueError as ve:
            print(f"Erreur format heure: {ve}")  # Debug
            return jsonify({"error": str(ve)}), 400

        # Créer le nouveau vol exactement comme dans pp.py
        nouveau_vol = {
            'TAXI_OUT': None,
            'AIR_TIME': None,
            'DISTANCE': float(data['DISTANCE']),
            'DAY': int(data['DAY']),
            'MONTH': int(data['MONTH']),
            'YEAR': int(data['YEAR']),
            'CRS_DEP_TIME_MIN': crs_dep_time_min,
            'DEP_TIME_MIN': dep_time_min,
            'CRS_ARR_TIME_MIN': crs_arr_time_min,
            'ORIGIN': data['ORIGIN'].upper(),
            'AIRLINE': data['AIRLINE'].upper(),
            'DEST': data['DEST'].upper()
        }

        # Calculer TAXI_OUT et AIR_TIME
        nouveau_vol['TAXI_OUT'] = nouveau_vol['DEP_TIME_MIN'] - nouveau_vol['CRS_DEP_TIME_MIN']
        nouveau_vol['AIR_TIME'] = nouveau_vol['CRS_ARR_TIME_MIN'] - nouveau_vol['DEP_TIME_MIN']

        print("Données formatées:", nouveau_vol)  # Debug

        # Utiliser la fonction predire_retard existante
        retard, duree_retard, cause_retard = predire_retard(nouveau_vol)

        print(f"Résultat prédiction: retard={retard}, durée={duree_retard}, cause={cause_retard}")  # Debug

        # Retourner le résultat
        if retard:
            response = {
                "retard": True,
                "duree": round(float(duree_retard), 2),
                "cause": CAUSES[int(cause_retard)]
            }
        else:
            response = {
                "retard": False,
                "duree": 0,
                "cause": ""
            }

        print("Réponse envoyée:", response)  # Debug
        return jsonify(response)

    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")  # Debug
        import traceback
        traceback.print_exc()  # Afficher la stack trace complète
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
