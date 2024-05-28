#!/bin/bash

# Lancer le backend
print("-----------------------------------------------------------------------)
print("Lancement du backend")
source antenv/bin/activate
print("-----------------------------------------------------------------------)
print("Antenv activé")
gunicorn --bind=0.0.0.0:$PORT app:app