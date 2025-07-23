# HBnB API

Une API REST pour le projet HBnB (clone d'AirBnB) utilisant Flask et Flask-RESTX.

## Structure du Projet

```
hbnb/
├── app/                    # Dossier principal de l'application
│   ├── api/               # Endpoints de l'API
│   │   ├── v1/           # Version 1 de l'API
│   │       ├── users.py   # Endpoints pour la gestion des utilisateurs
│   │       ├── places.py  # Endpoints pour la gestion des lieux
│   │       ├── reviews.py # Endpoints pour la gestion des avis
│   │       ├── amenities.py # Endpoints pour la gestion des commodités
│   ├── models/           # Modèles de données
│   │   ├── user.py      # Modèle utilisateur
│   │   ├── place.py     # Modèle lieu
│   │   ├── review.py    # Modèle avis
│   │   ├── amenity.py   # Modèle commodité
│   ├── services/        # Couche service (Pattern Facade)
│   │   ├── facade.py    # Implémentation du pattern Facade
│   ├── persistence/     # Couche de persistance
│       ├── repository.py # Implémentation du pattern Repository
├── run.py               # Point d'entrée de l'application
├── config.py           # Configuration de l'application
├── requirements.txt    # Dépendances du projet
```

## Description des Composants

### API (app/api/)
- Contient les endpoints REST organisés par version
- Utilise Flask-RESTX pour la documentation automatique Swagger
- Les endpoints sont séparés par domaine (users, places, reviews, amenities)

### Modèles (app/models/)
- Définit les classes métier de l'application
- Implémente la logique métier spécifique à chaque entité

### Services (app/services/)
- Implémente le pattern Facade pour simplifier l'interface entre l'API et la couche de persistance
- Gère la logique métier complexe et les interactions entre les différents composants

### Persistence (app/persistence/)
- Gère le stockage et la récupération des données
- Utilise le pattern Repository pour abstraire la source de données

## Installation

1. Cloner le repository :
```bash
git clone <repository-url>
cd hbnb
```

2. Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
venv\Scripts\activate     # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement de l'Application

1. Lancer l'application :
```bash
python run.py
```

2. Accéder à l'application :
- API : http://localhost:5000/api/v1/
- Documentation Swagger : http://localhost:5000/api/v1/

## Documentation API

La documentation complète de l'API est disponible via l'interface Swagger à l'adresse `/api/v1/`. 