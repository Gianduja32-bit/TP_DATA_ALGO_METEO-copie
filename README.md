# Weather CLI Application

Application météo en ligne de commande pour la ville de Toulouse.

**Version Python requise** : 3.12 ou supérieur.

## Démarrage Rapide

### Option 1 : Avec Docker (Recommandé)

1. **Construire l'image** :
   ```bash
   docker build -t weather-cli-app .
   ```

2. **Lancer l'application** :
   ```bash
   docker run -it weather-cli-app
   ```
   *Note : L'option `-it` est indispensable pour interagir avec le menu.*

---

### Option 2 : Sans Docker (Local)

1. **Créer et activer un environnement virtuel** :

   **Sur Mac/Linux :**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Sur Windows :**
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :
   ```bash
   python -m weather_cli
   ```

## Lancer les Tests

Pour exécuter la suite de tests unitaires :

```bash
pytest
```

Pour voir la couverture de code :

```bash
pytest --cov=weather_cli/src

```

## Rapport de Données (Profiling)

Un rapport détaillé sur les données météo peut être généré à l'aide de `ydata-profiling`.

### 1. Prérequis

Assurez-vous d'avoir installé les librairies nécessaires :

```bash
pip install pandas ydata-profiling
```

### 2. Générer le rapport

Pour générer le fichier `rapport.html`, exécutez le script suivant. Il est conseillé de se placer d'abord dans le dossier contenant les données pour que le script trouve le fichier CSV correctement.

```bash
cd weather_cli/src/data
python data_Profiling.py
```

### 3. Consulter le rapport

Une fois le script terminé, un fichier `rapport.html` sera créé dans le dossier `weather_cli/src/data`. Vous pouvez l'ouvrir avec n'importe quel navigateur web (Chrome, Firefox, Edge...) pour visualiser l'analyse complète des données.

---

## Design Patterns

| Pattern | Fichier | Description |
|---------|---------|-------------|
| **Singleton** | `weather_cli/src/infrastructure/config/settings.py` | Garantit une seule instance de la configuration. 
| **Decorator** | `weather_cli/src/services/display_service.py` | Enrichit l'affichage des données sans modifier les objets du domaine. 
| **Command** | `weather_cli/src/domain/commands/weather_commands.py` | Encapsule chaque étape du pipeline ETL dans une commande réutilisable. 

---

## Structures de Données

| Structure | Fichier | Description |
|-----------|---------|-------------|
| **Dictionnaire (Table de hachage)** | `weather_cli/src/domain/weather_dict.py` | Implémentation custom d'un dictionnaire utilisé comme cache des données météo. |
| **File (Liste chaînée)** | `weather_cli/src/domain/station_queue.py` | Implémentation custom d'une file FIFO pour naviguer entre les stations météo. |
