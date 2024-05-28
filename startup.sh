#!/bin/bash

# Lancer le backend
echo "-------------------------------------------------------------"
echo "Lancement du backend"
source antenv/bin/activate
echo "-------------------------------------------------------------"
echo "Antenv active"
gunicorn --bind=0.0.0.0:$PORT app:app