import pandas as pd
import joblib

# Fonction pour convertir le format hh:mm en minutes depuis minuit
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

# Fonction pour encoder les variables en chaîne (AIRLINE, ORIGIN, DEST)
def custom_target_encoder(df, col):
    if col in df.columns:
        mean = df.groupby(col).size().to_dict()  # Simple encodage basé sur la fréquence des valeurs
        df[f"{col}_ENCODED"] = df[col].map(mean)
        df = df.drop(columns=[col])
    return df

# Fonction principale pour prédire le retard
def predire_retard(nouveau_vol):
    # Convertir les temps de vol et horaires en minutes
    nouveau_vol['AIR_TIME'] = nouveau_vol['CRS_ARR_TIME_MIN'] - nouveau_vol['DEP_TIME_MIN']
    nouveau_vol['TAXI_OUT'] = nouveau_vol['DEP_TIME_MIN'] - nouveau_vol['CRS_DEP_TIME_MIN']
    # Appliquer l'encodage des variables manuelles (AIRLINE, ORIGIN, DEST)
    df_nouveau_vol = pd.DataFrame([nouveau_vol])
    df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'AIRLINE')
    df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'ORIGIN')
    df_nouveau_vol = custom_target_encoder(df_nouveau_vol, 'DEST')
    
    # Charger les modèles
    pipeline_clf = joblib.load('pipeline_clf.pkl')
    pipeline_reg = joblib.load('pipeline_reg.pkl')
    pipeline_cause = joblib.load('pipeline_cause.pkl')

    # Prédiction de la présence de retard
    retard_pred = pipeline_clf.predict(df_nouveau_vol)[0]
    
    # Si retard détecté, prédire la durée et la cause
    if retard_pred == 1:
        duree_retard_pred = pipeline_reg.predict(df_nouveau_vol)[0]
        cause_retard_pred = pipeline_cause.predict(df_nouveau_vol)[0]
        return True, duree_retard_pred, cause_retard_pred
    else:
        return False, None, None

# Fonction du menu utilisateur
def menu():
    print("Bienvenue dans le menu de prédiction des retards de vol !")
    
    # Demander à l'utilisateur d'entrer les informations du vol
    day = int(input("Jour du mois : "))
    month = int(input("Mois (1 à 12) : "))
    year = int(input("Année : "))
    crs_dep_time_min = input("Heure de départ prévue (hh:mm) : ")
    dep_time_min = input("Heure de départ réelle (hh:mm) : ")
    crs_arr_time_min = input("Heure d'arrivée prévue (hh:mm) : ")
    origin = input("Code aéroport de départ (ex: FFL) : ")
    airline = input("Code compagnie aérienne (ex: FFL) : ")
    dest = input("Code aéroport d'arrivée (ex: FFL) : ")
    
    # Convertir les heures en minutes depuis minuit
    crs_dep_time_min = time_to_minutes(crs_dep_time_min)
    dep_time_min = time_to_minutes(dep_time_min)
    crs_arr_time_min = time_to_minutes(crs_arr_time_min)
    
    # Créer un dictionnaire avec les données
    nouveau_vol = {
        'TAXI_OUT': None,  # Valeur à calculer
        'AIR_TIME': None,  # Valeur à calculer
        'DISTANCE': float(input("Distance (en kilomètres) : ")), 
        'DAY': day, 
        'MONTH': month, 
        'YEAR': year, 
        'CRS_DEP_TIME_MIN': crs_dep_time_min, 
        'DEP_TIME_MIN': dep_time_min,  
        'CRS_ARR_TIME_MIN': crs_arr_time_min, 
        'ORIGIN': origin, 
        'AIRLINE': airline, 
        'DEST': dest
    }
    
    # Appeler la fonction pour prédire les retards
    retard, duree_retard, cause_retard = predire_retard(nouveau_vol)
    
    # Affichage des résultats
    if retard:
        causes = ["Problème compagnie", "Météo", "Trafic aérien", "Retour au hangar", "Autre"]
        print("Retard : Oui")
        print(f"Durée du retard : {duree_retard} minutes")
        print(f"Cause du retard : {causes[cause_retard]}")
    else:
        print("Retard : Non")

menu()