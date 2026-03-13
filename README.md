# Deal Viewer - Système de Gestion de Deals

Un système complet de gestion de deals (affaires commerciales) avec gestion des contacts, templates personnalisés et affichage formaté. Built avec FastAPI et MongoDB pour le backend, Bootstrap 5.3 pour le frontend.

## Vue d'ensemble

Deal Viewer est une application web full-stack permettant aux équipes commerciales de :

-  Créer et gérer des deals (affaires commerciales)
-  Associer des contacts à chaque deal
-  Créer des templates d'affichage personnalisés
-  Ajouter des champs personnalisés dynamiquement
-  Visualiser les deals selon différents templates
-  Suivre l'état et les finances des deals (revenus estimés, marges)

##  Architecture

```
Deal_Viewer/
├── back/                          # Backend FastAPI
│   ├── src/
│   │   └── deal_viewer/
│   │       ├── config/            # Configuration (BD)
│   │       ├── controllers/       # Logique métier
│   │       ├── models/            # Modèles de données
│   │       ├── routes/            # Endpoints API
│   │       ├── schemas/           # Schémas de validation
│   │       ├── services/          # Services (CRUD)
│   │       ├── utils/             # Utilitaires
│   │       └── main.py            # Point d'entrée
│   ├── pyproject.toml             # Dépendances Python
│   └── README.md
│
└── front/                         # Frontend Web
    ├── index.html                 # Interface HTML
    ├── app.js                     # JavaScript (Vanilla)
    └── (CSS Bootstrap intégré)
```

##  Technologies utilisées

### Backend
- **Framework**: FastAPI (Python)
- **Base de données**: MongoDB
- **Validation**: Pydantic
- **Serveur**: Uvicorn

### Frontend
- **Framework CSS**: Bootstrap 5.3
- **Framework JS**: Vanilla JavaScript (ES6+)
- **Icons**: Bootstrap Icons 1.11.0
- **HTTP Client**: Fetch API

##  Prérequis

- **Python 3.8+**
- **Poetry** (gestionnaire de dépendances Python)
- **MongoDB** (local ou cloud)
- **Node.js** (optionnel, pour serveur le frontend)

##  Installation

### 1. Cloner le repository

```bash
git clone <votre-repo>
cd Deal_Viewer
```

### 2. Configuration Backend

#### a. Naviguer vers le dossier backend
```bash
cd back
```

#### b. Installer les dépendances avec Poetry
```bash
poetry install
```

#### c. Configurer les variables d'environnement

Créer un fichier `.env` dans le dossier `back/` :

```env
# MongoDB Configuration
MONGODB_URI=adresse vers la database
DATABASE_NAME=nom de la base de donnée



#### d. Démarrer le serveur backend
```bash
poetry run uvicorn src.deal_viewer.main:app --reload
```

Le backend sera accessible à : `http://127.0.0.1:8000`

### 3. Configuration Frontend

#### a. Naviguer vers le dossier frontend
```bash
cd front
```

#### b. Démarrer un serveur web (Python intégré)
```bash
python -m http.server 8080
```

Ou avec Node.js (si installé) :
```bash
npx http-server -p 8080
```

Le frontend sera accessible à : `http://127.0.0.1:8080`

##  Utilisation

### Démarrage rapide

1. **Terminal 1** - Backend :
   ```bash
   cd back
   poetry run uvicorn src.deal_viewer.main:app --reload
   ```

2. **Terminal 2** - Frontend :
   ```bash
   cd front
   python -m http.server 8080
   ```

3. **Ouvrir le navigateur** :
   ```
   http://127.0.0.1:8080
   ```

### Fonctionnalités principales

####  Gestion des Deals (Onglet 1)

**Créer un Deal:**
1. Remplir les informations obligatoires :
   - Référence et Titre
   - Statut (Nouveau, En cours, Gagné, Perdu, En attente)
   - Informations client (Nom, Pays, Ville)
   - Propriétaire (Nom, Email)
   - Finances (Devise, Revenu estimé, Marge %)
   - **Contacts** (Prénom, Nom, Poste, Email, Décideur)

2. Cliquer "Créer Deal"

**Modifier un Deal:**
1. Cliquer sur "Modifier" sur le deal souhaité
2. Adapter les informations
3. Gérer les contacts existants ou en ajouter de nouveaux
4. Ajouter/supprimer des champs personnalisés
5. Cliquer "Mettre à Jour"

**Supprimer un Deal:**
- Cliquer "Supprimer" et confirmer

####  Gestion des Templates (Onglet 2)

**Créer un Template:**
1. Donner un nom et une description
2. Définir les champs visibles (JSON array)
3. Définir les sections (JSON array avec structure)
4. Cliquer "Créer Template"

**Exemple de Template JSON:**
```json
{
  "visibleFields": ["title", "clientName", "status", "estimatedRevenue"],
  "sections": [
    {
      "name": "Informations",
      "fields": ["title", "reference", "status"]
    },
    {
      "name": "Client",
      "fields": ["clientName", "country"]
    },
    {
      "name": "Finances",
      "fields": ["estimatedRevenue", "currency"]
    }
  ]
}
```

####  Affichage Formaté (Onglet 3)

1. Sélectionner un template
2. Cliquer "Afficher les Deals"
3. Les deals s'affichent selon le format du template

## Structure des données

### Deal Model

```python
{
  "reference": str,                 # Unique identifier
  "title": str,
  "status": str,                    # new, in_progress, won, lost, held
  "clientName": str,
  "country": str,
  "city": str,
  "ownerName": str,
  "ownerEmail": str,                # Valid email
  "currency": str,                  # EUR, USD, GBP
  "estimatedRevenue": float,
  "estimatedMargin": float,
  "contacts": [                     # At least one contact required
    {
      "firstName": str,
      "lastName": str,
      "jobTitle": str,
      "email": str,
      "isDecisionMaker": bool
    }
  ],
  "createdAt": datetime,            # Auto-generated
  "customField1": str,              # Optional custom fields
  "customField2": str
}
```

### Template Model

```python
{
  "name": str,
  "description": str,
  "visibleFields": [str],           # List of field names to display
  "sections": [
    {
      "name": str,
      "fields": [str]               # Fields in this section
    }
  ],
  "labels": {str: str}              # Field labels mapping
}
```

## 🔌 API Endpoints

### Deals

```
POST   /deals/                      # Create deal
GET    /deals/                      # Get all deals
GET    /deals/{deal_id}             # Get specific deal
PUT    /deals/{deal_id}             # Update deal
DELETE /deals/{deal_id}             # Delete deal
PUT    /deals/{deal_id}/fields      # Delete custom fields
```

### Templates

```
POST   /templates/                  # Create template
GET    /templates/                  # Get all templates
GET    /templates/{template_id}     # Get specific template
PUT    /templates/{template_id}     # Update template
DELETE /templates/{template_id}     # Delete template
```

### System

```
GET    /health-check/               # Health check endpoint
POST   /deals/?template_name=xxx    # Get formatted deals
```

##  Validation et Règles métier

### Champs obligatoires (Deal)
- `reference` - Unique dans la base
- `title`
- `status`
- `clientName`
- `country`, `city`
- `ownerName`, `ownerEmail` (email valide)
- `currency` (EUR, USD, GBP)
- `estimatedRevenue`, `estimatedMargin`
- `contacts` - **Au moins un contact complet requis**

### Champs obligatoires (Contact)
- `firstName`
- `lastName`
- `jobTitle`
- `email` (email valide)
- `isDecisionMaker`

### Champs personnalisés
-  Peuvent être ajoutés dynamiquement
-  Ne peuvent pas dupliquer les noms des champs requis
-  Ne peuvent pas avoir deux champs avec le même nom
-  Peuvent être supprimés à tout moment

##  Troubleshooting

### Backend ne démarre pas
```bash
# Vérifier que Poetry est installé
poetry --version

# Réinstaller les dépendances
poetry install

# Vérifier la connexion MongoDB
# Editer .env avec la bonne URI
```

### Frontend ne se connecte pas au backend
- Vérifier que le backend tourne sur `http://127.0.0.1:8000`
- Vérifier la console du navigateur (F12) pour les erreurs CORS
- Vérifier que les deux services sont sur les bons ports (8080 frontend, 8000 backend)

### MongoDB connection error
```bash
# Vérifier que MongoDB tourne localement
# Ou éditer .env avec une URI Atlas valide
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/
```

##  Fichiers de configuration

### `.env` (Backend)
À créer dans `back/` avec vos paramètres MongoDB

### `pyproject.toml` (Backend)
Définit les dépendances Python et métadonnées du projet

