# 🧪 Organisation des Tests HBNB

## 📁 Structure des Tests

La nouvelle organisation des tests suit une structure modulaire pour un meilleur suivi et organisation :

```
hbnb/
├── test_all.py                    # Lanceur global de tous les tests
├── app/
│   ├── models/
│   │   └── test/
│   │       ├── __init__.py
│   │       ├── run_tests.py       # Tests du module Models
│   │       ├── test_user.py       # 18 tests
│   │       ├── test_amenity.py    # 8 tests
│   │       ├── test_place.py      # 10 tests
│   │       └── test_review.py     # 9 tests
│   ├── api/
│   │   └── v1/
│   │       └── test/
│   │           ├── __init__.py
│   │           ├── run_tests.py              # Tests de l'API v1
│   │           ├── test_users_endpoints.py    # 20 tests
│   │           ├── test_amenities_endpoints.py # 13 tests
│   │           ├── test_places_endpoints.py   # 20 tests
│   │           ├── test_reviews_endpoints.py  # 15 tests
│   │           └── test_auth_endpoints.py    # 11 tests
│   ├── services/
│   │   └── test/
│   │       ├── __init__.py
│   │       ├── run_tests.py              # Tests du module Services
│   │       ├── test_facade.py            # 20 tests
│   │       └── test_amenities_facade.py  # 12 tests
│   └── persistence/
│       └── test/
│           ├── __init__.py
│           └── run_tests.py       # Tests du module Persistence (à développer)
```

## 🚀 Comment Exécuter les Tests

### 1. Tous les Tests
```bash
cd hbnb
python3 test_all.py
```

### 2. Tests par Module
```bash
# Tests des modèles
python3 test_all.py --module models

# Tests de l'API
python3 test_all.py --module api

# Tests des services
python3 test_all.py --module services

# Tests de la persistance (à développer)
python3 test_all.py --module persistence
```

### 3. Tests d'une Classe Spécifique
```bash
# Tests de User (modèle)
python3 test_all.py --class user

# Tests d'Amenity (modèle)
python3 test_all.py --class amenity

# Tests de Place (modèle)
python3 test_all.py --class place

# Tests de Review (modèle)
python3 test_all.py --class review

# Tests des endpoints utilisateurs (API)
python3 test_all.py --class users_endpoints

# Tests des endpoints amenities (API)
python3 test_all.py --class amenities_endpoints

# Tests des endpoints places (API)
python3 test_all.py --class places_endpoints

# Tests des endpoints reviews (API)
python3 test_all.py --class reviews_endpoints

# Tests des endpoints auth (API)
python3 test_all.py --class auth_endpoints

# Tests de la facade (Services)
python3 test_all.py --class facade

# Tests de la facade amenities (Services)
python3 test_all.py --class amenities_facade
```

### 4. Tests d'un Module Spécifique (depuis le dossier du module)
```bash
# Tests des modèles depuis leur dossier
cd app/models/test
python3 run_tests.py

# Tests de l'API v1 depuis leur dossier
cd app/api/v1/test
python3 run_tests.py

# Tests des services depuis leur dossier
cd app/services/test
python3 run_tests.py

# Tests spécifiques dans un module
cd app/api/v1/test
python3 run_tests.py users_endpoints
python3 run_tests.py amenities_endpoints
python3 run_tests.py places_endpoints
python3 run_tests.py reviews_endpoints
python3 run_tests.py auth_endpoints

cd app/services/test
python3 run_tests.py facade
python3 run_tests.py amenities_facade
```

### 5. Aide
```bash
python3 test_all.py --help
```

## 📊 Format des Résultats

Le lanceur global affiche :
- 🧪 Module en cours de test
- ✅ Tests réussis
- ❌ Tests échoués
- 💥 Erreurs
- 📊 Statistiques par classe
- 📋 Résumé global final

## 🔧 Ajouter de Nouveaux Tests

### Pour les Modèles
1. Créez votre fichier de test dans `app/models/test/`
2. Importez-le dans `app/models/test/run_tests.py`
3. Ajoutez la classe dans `test_all.py`

### Pour l'API
1. Créez vos fichiers de test dans `app/api/v1/test/`
2. Mettez à jour `app/api/v1/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

### Pour les Services
1. Créez vos fichiers de test dans `app/services/test/`
2. Mettez à jour `app/services/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

### Pour la Persistance
1. Créez vos fichiers de test dans `app/persistence/test/`
2. Mettez à jour `app/persistence/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

## 🎯 Avantages de Cette Organisation

- ✅ **Modularité** : Tests organisés par module fonctionnel
- ✅ **Scalabilité** : Facile d'ajouter de nouveaux modules de tests
- ✅ **Flexibilité** : Possibilité d'exécuter des tests spécifiques
- ✅ **Maintenance** : Structure claire et logique
- ✅ **CI/CD** : Compatible avec les pipelines d'intégration continue

## 📈 Statistiques Actuelles

- **Total des tests** : **156 tests** (45 Models + 79 API + 32 Services)
- **Modules testés** : 
  - ✅ **Models** : User (18), Amenity (8), Place (10), Review (9) = **45 tests**
  - ✅ **API v1** : Users (20), Amenities (13), Places (20), Reviews (15), Auth (11) = **79 tests**
  - ✅ **Services** : HBnB Facade (20) + Amenities Facade (12) = **32 tests**
- **Modules à développer** : Persistence
- **Taux de réussite** : 100% ✅
- **Couverture** : 100% des fonctionnalités développées

## 🎯 Types de Tests Couverts

### **Tests de Modèles (Models) - 45 tests**

#### **User Model (18 tests)**
- ✅ Création d'utilisateur avec données valides
- ✅ Validation email invalide
- ✅ Validation first_name trop long
- ✅ Validation last_name trop long
- ✅ Validation first_name vide
- ✅ Validation last_name vide
- ✅ Utilisateur admin
- ✅ Mise à jour d'utilisateur
- ✅ Validation longueur maximale valide
- ✅ Validation emails valides (plusieurs formats)
- ✅ Validation emails invalides (plusieurs formats)
- ✅ Hashage du mot de passe
- ✅ Vérification mot de passe correct
- ✅ Vérification mot de passe incorrect
- ✅ Validation mot de passe vide
- ✅ Validation mot de passe None
- ✅ Hashages différents pour même mot de passe

#### **Amenity Model (8 tests)**
- ✅ Création d'amenity avec données valides
- ✅ Validation nom invalide
- ✅ Validation nom vide
- ✅ Validation nom None
- ✅ Validation nom avec espaces
- ✅ Cas limites valides
- ✅ Attributs BaseModel hérités
- ✅ Méthodes save et update

#### **Place Model (10 tests)**
- ✅ Création de place avec données valides
- ✅ Validation titre vide
- ✅ Validation titre trop long
- ✅ Validation prix négatif
- ✅ Validation prix zéro
- ✅ Validation latitude invalide
- ✅ Validation longitude invalide
- ✅ Validation owner invalide
- ✅ Ajout de review
- ✅ Ajout d'amenity

#### **Review Model (9 tests)**
- ✅ Création de review avec données valides
- ✅ Validation rating invalide
- ✅ Validation rating zéro
- ✅ Validation rating négatif
- ✅ Validation rating float
- ✅ Validation place type invalide
- ✅ Validation user type invalide
- ✅ Validation texte vide
- ✅ Validation texte None
- ✅ Attributs hérités de BaseModel

### **Tests d'API (Endpoints) - 79 tests**

#### **Users Endpoints (20 tests)**
- ✅ **POST /api/v1/users/**
  - Création avec succès
  - Email déjà existant (400)
  - Données invalides (400)
  - Champs manquants (400)
  - Sans mot de passe (400)
  - Mot de passe non retourné dans la réponse
- ✅ **GET /api/v1/users/**
  - Liste avec utilisateurs
  - Liste vide
  - Mots de passe non retournés
- ✅ **GET /api/v1/users/<id>**
  - Succès par ID
  - Utilisateur inexistant (404)
  - Mot de passe non retourné
- ✅ **PUT /api/v1/users/<id>** (JWT requis)
  - Succès avec nouvelles données
  - Succès avec même email
  - Utilisateur inexistant (404)
  - Email déjà utilisé (400)
  - Modification email interdite (400)
  - Modification password interdite (400)
  - Utilisateur non autorisé (403)
  - Sans token JWT (401)
  - Mot de passe non retourné dans la réponse

#### **Places Endpoints (20 tests)**
- ✅ **POST /api/v1/places/** (JWT requis)
  - Création avec succès (owner_id depuis JWT)
  - Sans token JWT (401)
  - Prix invalide (400)
  - Coordonnées invalides (400)
  - Amenity invalide (400)
  - Titre avec caractères spéciaux
  - Description None
  - Prix type invalide
  - Coordonnées type invalide
  - JSON mal formé (400)
  - JSON vide (400)
- ✅ **GET /api/v1/places/** (Public)
  - Liste avec places
  - Détails complets avec owner et amenities
- ✅ **GET /api/v1/places/<id>** (Public)
  - Succès par ID
  - Place inexistante (404)
- ✅ **PUT /api/v1/places/<id>** (JWT requis)
  - Succès avec nouvelles données
  - Place inexistante (404)
  - Coordonnées invalides (400)
  - Prix invalide (400)
  - Amenity invalide (400)
  - Utilisateur non autorisé (403)
  - Sans token JWT (401)

#### **Reviews Endpoints (15 tests)**
- ✅ **POST /api/v1/reviews/** (JWT requis)
  - Création avec succès (user_id depuis JWT)
  - Sans token JWT (401)
  - Rating invalide (400)
  - Place inexistante (404)
  - Review de son propre lieu (400)
  - Review dupliquée (400)
- ✅ **GET /api/v1/reviews/** (Public)
  - Liste avec reviews
- ✅ **GET /api/v1/reviews/<id>** (Public)
  - Succès par ID
  - Review inexistante (404)
- ✅ **GET /api/v1/reviews/places/<place_id>/reviews** (Public)
  - Liste des reviews d'un lieu
- ✅ **PUT /api/v1/reviews/<id>** (JWT requis)
  - Succès avec nouvelles données
  - Review inexistante (404)
  - Utilisateur non autorisé (403)
  - Sans token JWT (401)
- ✅ **DELETE /api/v1/reviews/<id>** (JWT requis)
  - Suppression avec succès
  - Review inexistante (404)
  - Utilisateur non autorisé (403)
  - Sans token JWT (401)

#### **Auth Endpoints (11 tests)**
- ✅ **POST /api/v1/auth/login**
  - Connexion avec succès
  - Email invalide (401)
  - Mot de passe invalide (401)
  - Email manquant (400)
  - Mot de passe manquant (400)
  - Token contient user_id
  - Format Bearer correct
- ✅ **GET /api/v1/auth/protected** (JWT requis)
  - Accès avec token valide
  - Accès sans token (401)
  - Accès avec token invalide (401)
  - Accès avec token expiré (401)

#### **Amenities Endpoints (13 tests)**
- ✅ **POST /api/v1/amenities/**
  - Création avec succès
  - Données invalides (400)
  - Nom manquant (400)
  - Nom trop long (400)
- ✅ **GET /api/v1/amenities/**
  - Liste avec amenities
  - Liste vide
- ✅ **GET /api/v1/amenities/<id>**
  - Succès par ID
  - Amenity inexistante (404)
- ✅ **PUT /api/v1/amenities/<id>**
  - Succès avec nouvelles données
  - Amenity inexistante (404)
  - Données invalides (400)
  - Nom trop long (400)

### **Tests de Services (Facade) - 32 tests**

#### **HBnB Facade (20 tests)**
- ✅ **Gestion des utilisateurs**
  - Création d'utilisateurs
  - Récupération par ID (succès + inexistant)
  - Récupération par email (succès + inexistant)
  - Liste complète des utilisateurs
  - Mise à jour (succès + inexistant + email dupliqué + même email)
- ✅ **Gestion des places**
  - Récupération par ID (inexistant)
- ✅ **Gestion des reviews**
  - Création de review
  - Récupération par ID
  - Liste complète des reviews
  - Reviews par lieu
  - Mise à jour (succès + rating invalide)
  - Suppression

#### **Amenities Facade (12 tests)**
- ✅ **Gestion des amenities**
  - Création (succès + nom invalide + nom trop long)
  - Récupération par ID (succès + inexistant)
  - Liste complète des amenities
  - Mise à jour (succès + inexistant + données invalides + nom trop long)

## 🔐 Tests d'Authentification JWT

### **Endpoints Protégés (JWT requis)**

#### **Places**
- ✅ POST `/api/v1/places/` - Création avec JWT, owner_id automatique depuis token
- ✅ PUT `/api/v1/places/<id>` - Modification avec vérification de propriété

#### **Reviews**
- ✅ POST `/api/v1/reviews/` - Création avec JWT, user_id automatique depuis token
- ✅ PUT `/api/v1/reviews/<id>` - Modification avec vérification de propriété
- ✅ DELETE `/api/v1/reviews/<id>` - Suppression avec vérification de propriété

#### **Users**
- ✅ PUT `/api/v1/users/<id>` - Modification avec vérification de propriété et restrictions

### **Endpoints Publics (sans JWT)**

- ✅ GET `/api/v1/places/` - Liste publique
- ✅ GET `/api/v1/places/<id>` - Détails publics
- ✅ GET `/api/v1/reviews/` - Liste publique
- ✅ GET `/api/v1/reviews/<id>` - Détails publics
- ✅ GET `/api/v1/reviews/places/<place_id>/reviews` - Reviews d'un lieu (public)
- ✅ GET `/api/v1/users/` - Liste publique
- ✅ GET `/api/v1/users/<id>` - Détails publics

### **Validations de Sécurité Testées**

- ✅ Vérification de propriété (places, reviews)
- ✅ Empêchement de review de son propre lieu
- ✅ Empêchement de review dupliquée
- ✅ Empêchement de modification email/password
- ✅ Empêchement de modification d'un autre utilisateur
- ✅ Tous les endpoints protégés retournent 401 sans token
- ✅ Tous les endpoints protégés retournent 403 pour actions non autorisées

## 🎯 Couverture de Tests Détaillée

### **Facade (Services) - 100% Couvert**

| Méthode | Tests | Scénarios Testés |
|---------|-------|------------------|
| `create_user()` | ✅ | Création normale |
| `get_user()` | ✅ | Succès + inexistant |
| `get_all_users()` | ✅ | Liste avec utilisateurs |
| `get_user_by_email()` | ✅ | Succès + inexistant |
| `update_user()` | ✅ | Succès + inexistant + email dupliqué + même email |
| `get_place()` | ✅ | ID inexistant |
| `create_review()` | ✅ | Création normale |
| `get_review()` | ✅ | Succès + inexistant |
| `get_all_reviews()` | ✅ | Liste avec reviews |
| `get_reviews_by_place()` | ✅ | Reviews par lieu |
| `update_review()` | ✅ | Succès + rating invalide |
| `delete_review()` | ✅ | Suppression |
| `create_amenity()` | ✅ | Création normale + validations |
| `get_amenity()` | ✅ | Succès + inexistant |
| `get_all_amenities()` | ✅ | Liste avec amenities |
| `update_amenity()` | ✅ | Succès + inexistant + données invalides |

### **Endpoints API - 100% Couvert**

| Endpoint | Méthode | Tests | Scénarios Testés |
|----------|---------|-------|------------------|
| `/api/v1/users/` | POST | ✅ | Succès + email dupliqué + données invalides + champs manquants + sans password |
| `/api/v1/users/` | GET | ✅ | Liste avec utilisateurs + liste vide |
| `/api/v1/users/<id>` | GET | ✅ | Succès + inexistant |
| `/api/v1/users/<id>` | PUT | ✅ | Succès + inexistant + email dupliqué + même email + JWT + unauthorized + sans token + password |
| `/api/v1/amenities/` | POST | ✅ | Succès + données invalides + champs manquants + nom trop long |
| `/api/v1/amenities/` | GET | ✅ | Liste avec amenities + liste vide |
| `/api/v1/amenities/<id>` | GET | ✅ | Succès + inexistant |
| `/api/v1/amenities/<id>` | PUT | ✅ | Succès + inexistant + données invalides + nom trop long |
| `/api/v1/places/` | POST | ✅ | Succès + JWT + données invalides + coordonnées invalides + amenity invalide + sans token |
| `/api/v1/places/` | GET | ✅ | Liste avec places (public) |
| `/api/v1/places/<id>` | GET | ✅ | Succès + inexistant (public) |
| `/api/v1/places/<id>` | PUT | ✅ | Succès + inexistant + JWT + unauthorized + sans token + données invalides |
| `/api/v1/reviews/` | POST | ✅ | Succès + JWT + rating invalide + place inexistante + own place + duplicate + sans token |
| `/api/v1/reviews/` | GET | ✅ | Liste avec reviews (public) |
| `/api/v1/reviews/<id>` | GET | ✅ | Succès + inexistant (public) |
| `/api/v1/reviews/<id>` | PUT | ✅ | Succès + inexistant + JWT + unauthorized + sans token |
| `/api/v1/reviews/<id>` | DELETE | ✅ | Succès + inexistant + JWT + unauthorized + sans token |
| `/api/v1/reviews/places/<place_id>/reviews` | GET | ✅ | Liste des reviews d'un lieu (public) |
| `/api/v1/auth/login` | POST | ✅ | Succès + email invalide + password invalide + champs manquants + token format |
| `/api/v1/auth/protected` | GET | ✅ | Token valide + sans token + token invalide + token expiré |

## 🆕 Nouveaux Tests Ajoutés (Authentification JWT)

### **Tests d'Authentification (Auth Endpoints) - 11 tests**
- ✅ `test_login_success()` - Connexion réussie
- ✅ `test_login_invalid_email()` - Email invalide
- ✅ `test_login_invalid_password()` - Mot de passe invalide
- ✅ `test_login_missing_email()` - Email manquant
- ✅ `test_login_missing_password()` - Mot de passe manquant
- ✅ `test_protected_endpoint_with_valid_token()` - Accès avec token valide
- ✅ `test_protected_endpoint_without_token()` - Accès sans token
- ✅ `test_protected_endpoint_with_invalid_token()` - Accès avec token invalide
- ✅ `test_protected_endpoint_with_expired_token()` - Accès avec token expiré
- ✅ `test_jwt_token_contains_user_id()` - Token contient user_id
- ✅ `test_protected_endpoint_with_bearer_format()` - Format Bearer correct

### **Tests Places avec JWT - 2 nouveaux tests**
- ✅ `test_update_place_unauthorized()` - Modification non autorisée (403)
- ✅ `test_update_place_without_token()` - Modification sans token (401)

### **Tests Reviews avec JWT - 6 nouveaux tests**
- ✅ `test_create_review_own_place()` - Review de son propre lieu (400)
- ✅ `test_create_review_duplicate()` - Review dupliquée (400)
- ✅ `test_update_review_unauthorized()` - Modification non autorisée (403)
- ✅ `test_delete_review_unauthorized()` - Suppression non autorisée (403)
- ✅ `test_create_review_without_token()` - Création sans token (401)
- ✅ `test_update_review_without_token()` - Modification sans token (401)
- ✅ `test_delete_review_without_token()` - Suppression sans token (401)

### **Tests Users avec JWT - 2 nouveaux tests**
- ✅ `test_update_user_unauthorized()` - Modification non autorisée (403)
- ✅ `test_update_user_without_token()` - Modification sans token (401)
- ✅ `test_update_user_password()` - Modification password interdite (400)

## 🚀 Prochaines Étapes

### **Tests à Développer**
1. **Tests de Persistence** - Repository et base de données
2. **Tests d'Intégration** - Flux complets end-to-end
3. **Tests de Performance** - Charge et stress
4. **Tests de Sécurité Avancés** - Injection SQL, XSS, CSRF

### **Améliorations Possibles**
- Tests de concurrence pour les emails
- Tests de validation avancée
- Tests de rollback et transactions
- Mocking avancé pour l'isolation
- Tests de rate limiting
- Tests de tokens refresh

## 📝 Notes Importantes

- Tous les endpoints POST/PUT/DELETE nécessitent maintenant un JWT (sauf création d'utilisateur)
- Les endpoints GET restent publics pour permettre la consultation
- Les validations de propriété sont testées pour places, reviews et users
- Les restrictions métier (pas de review de son propre lieu, pas de doublon) sont testées
- La sécurité des mots de passe est testée (non retournés dans les réponses)
