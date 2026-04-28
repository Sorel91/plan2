# Analyse du dépôt `Graph2Plan`

## Vue d’ensemble
Ce dépôt implémente **Graph2Plan**, un pipeline de génération de plans d’étage à partir de graphes de pièces et de contraintes de frontière.

Le projet est organisé en 4 blocs principaux :

1. `DataPreparation/` : scripts de conversion/ingénierie de données RPLAN vers formats d’entraînement et de recherche.
2. `Network/` : entraînement du modèle deep learning (PyTorch + Ignite).
3. `PostProcess/` : exécution hors interface (inférence, alignement, décoration).
4. `Interface/` : application Django interactive avec édition de graphes côté utilisateur.

## Architecture fonctionnelle

### 1) Préparation des données
Le README de `DataPreparation` décrit une chaîne en 6 scripts (turning functions, conversion train/test, statistiques de rooms, clustering FAISS). Le résultat alimente à la fois la récupération (retrieval) et les jeux d’entraînement.

### 2) Entraînement réseau
`Network/train.py` expose :
- un parseur riche d’hyperparamètres (données, architecture, pertes, optimisation, checkpoints) ;
- des DataLoaders pour `train/valid/test` à partir de `.mat` ;
- un entraînement combinant génération de layout et raffinement de bounding boxes.

`Network/split.py` réalise un split 70/15/15 du `data.mat` vers `data_train.mat`, `data_valid.mat`, `data_test.mat`.

### 3) Pipeline d’inférence/post-processing
Dans `PostProcess/app.py`, la classe `App` encapsule :
- chargement du modèle et de la base de retrieval ;
- retrieval des candidats proches ;
- transfert/adaptation du graphe au contour cible ;
- forward du réseau (layout + boxes) ;
- alignement géométrique et ajout portes/fenêtres.

### 4) Interface Django
`Interface/Houseweb/views.py` gère :
- l’initialisation (chargement données train/test, moteur Matlab, modèle, retrieval) ;
- la recherche par contraintes (nombre/type de pièces) ;
- la récupération de plans candidats et la sérialisation vers le frontend.

## Dépendances et contraintes techniques
- **Python + PyTorch** pour entraînement et inférence.
- **Django** pour l’interface web.
- **Matlab Engine for Python** requis pour l’alignement géométrique des boîtes (`align_fp`).
- Données externes volumineuses (RPLAN prétraité, `.npy/.pkl/.mat`) nécessaires pour un run complet.

## Points forts
- Séparation claire entre préparation, entraînement, post-traitement et interface.
- Pipeline de retrieval + génération + alignement bien structuré.
- Mode application (`PostProcess/app.py`) simple à réutiliser hors GUI.

## Risques / dette technique
- Forte dépendance à Matlab : point de friction pour déploiement Linux/cloud.
- Présence de nombreux artefacts binaires/versionnés (`.pyc`, `model.pth`, `db.sqlite3`) qui alourdissent le dépôt.
- Plusieurs scripts avec hypothèses de chemins relatives (fragiles en CI/CD).
- Utilisation d’API legacy (`time.clock`) dans l’interface, dépréciée en Python moderne.

## Recommandations prioritaires
1. **Industrialiser l’environnement** : ajouter un `requirements.txt`/`environment.yml` par sous-module et scripts de bootstrap.
2. **Nettoyer le versionnement** : ignorer artefacts binaires et caches Python via `.gitignore`.
3. **Compatibilité Python moderne** : remplacer `time.clock()` par `time.perf_counter()`.
4. **Découpler Matlab** (à moyen terme) : abstraction d’alignement pour fallback pure Python.
5. **Tests de non-régression** : smoke tests CLI pour `split.py`, chargement modèle, et endpoint d’initialisation Django.

## Conclusion
Le dépôt est une base de recherche solide et relativement modulaire, avec un vrai produit démonstrateur (GUI). Pour usage production/équipe élargie, l’effort principal porte sur la reproductibilité d’environnement, la réduction des dépendances lourdes (Matlab), et l’hygiène repository/CI.
