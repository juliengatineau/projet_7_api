#!/bin/bash

# Lancer le backend
echo "-------------------------------------------------------------"
echo "Lancement du backend"

echo "-------------------------------------------------------------"
echo "Environnement actif : $VIRTUAL_ENV"

source antenv/bin/activate
echo "-------------------------------------------------------------"
echo "Antenv active"
echo "-------------------------------------------------------------"

echo "Environnement actif : $VIRTUAL_ENV"
echo "-------------------------------------------------------------"
echo "Liste des bibliothèques installées :"
pip freeze
echo "-------------------------------------------------------------"
if [ -f requirements.txt ]; then
    echo "Le fichier requirements.txt a été trouvé."
    echo "Installation des dépendances à partir de requirements.txt..."
    pip install -r requirements.txt
else
    echo "Le fichier requirements.txt n'a pas été trouvé."
fi
echo "-------------------------------------------------------------"
echo "Liste des bibliothèques installées :"
pip freeze
gunicorn --bind=0.0.0.0:$PORT app:app