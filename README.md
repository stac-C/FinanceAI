# FinanceAI - Application de Prédiction Financière

Application Django pour la prédiction de défauts de prêt utilisant le machine learning.

## Déploiement sur Vercel

### Configuration des Variables d'Environnement

Dans le dashboard Vercel, configurez les variables suivantes :

- `SECRET_KEY` : Une clé secrète Django (générez-en une avec `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- `DEBUG` : `False` (pour la production)
- `ALLOWED_HOSTS` : `votre-app.vercel.app` (remplacez par votre domaine Vercel)
- `DATABASE_URL` : `db.sqlite3` (ou une URL de base de données externe)

### Déploiement Automatique

1. Connectez votre repository GitHub à Vercel
2. Vercel détectera automatiquement la configuration Django
3. Le déploiement se fera automatiquement à chaque push

### Commandes de Build

Le fichier `vercel.json` configure :
- Installation des dépendances
- Exécution des migrations
- Collecte des fichiers statiques

### Base de Données

⚠️ **Note importante** : SQLite n'est pas recommandé pour la production sur Vercel car le stockage est éphémère. Pour un usage en production, utilisez PostgreSQL via un add-on Vercel ou une base de données externe.