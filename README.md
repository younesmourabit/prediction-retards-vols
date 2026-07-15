# ✈️ Flight Delay Prediction using Machine Learning

## Description

Ce projet consiste à développer une application web permettant de prédire les retards de vols à l'aide des techniques de **Machine Learning**.

L'application analyse les caractéristiques d'un vol afin d'estimer si celui-ci sera retardé ou non. Elle offre une interface simple développée avec **Flask**, permettant aux utilisateurs de réaliser des prédictions en temps réel.

---

## Objectifs

- Prédire les retards de vols avec une bonne précision.
- Comparer différents modèles de Machine Learning.
- Développer une application web interactive.
- Aider les compagnies aériennes à anticiper les retards.

---

##  Fonctionnalités

-  Nettoyage et préparation des données
-  Entraînement de modèles de Machine Learning
-  Prédiction des retards de vols
-  Interface Web développée avec Flask
-  Analyse exploratoire des données
-  Sauvegarde des modèles entraînés

---

## Technologies utilisées

- Python
- Flask
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- Jupyter Notebook
- HTML
- CSS
- JavaScript

---

##  Structure du projet

```
prediction-retards-vols
│
├── FINAL_MODEL_TRAIN-Copy1.ipynb
├── flas.py
├── rapport.py
├── pp.py
├── pipeline_clf.pkl
├── pipeline_reg.pkl
├── pipeline_cause.pkl
├── flight_delay_profiling_report.html
├── avion.jpg
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── index.html
├── Younes MOURABIT.pptx
└── README.md
```

---

##  Base de données

Le projet s'appuie sur une base de données contenant plusieurs millions d'enregistrements de vols.

Les principales étapes de préparation des données sont :

- Suppression des doublons
- Gestion des valeurs manquantes
- Transformation des dates
- Encodage des variables catégorielles
- Sélection des variables pertinentes
- Prétraitement avant l'entraînement

> **Remarque :** Le fichier de données complet n'est pas inclus dans ce dépôt en raison de sa taille.

---

##  Modèles de Machine Learning

Plusieurs modèles ont été testés :

- ✅ XGBoost
- MLP Regressor
- Pipeline Scikit-learn

Le modèle **XGBoost** a offert les meilleures performances pour la prédiction des retards de vols.

---

## 🌐 Application Web

L'application permet de :

- saisir les informations d'un vol ;
- lancer une prédiction ;
- afficher instantanément le résultat.

---

##  Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/younesmourabit/prediction-retards-vols.git
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python flas.py
```

### 4. Ouvrir dans le navigateur

```
http://127.0.0.1:5000
```

---

## 📈 Résultats

Le projet montre que l'utilisation du Machine Learning permet d'améliorer l'anticipation des retards de vols.

Le modèle **XGBoost** s'est révélé être le plus performant parmi les modèles évalués.

---

##  Auteur

**Younes MOURABIT**

🎓 Master Systèmes d'Information Décisionnel et Imagerie (SIDI)

Université Moulay Ismaïl

---

## 📄 Licence

Ce projet est réalisé dans un cadre académique.
