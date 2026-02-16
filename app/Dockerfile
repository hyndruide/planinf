# syntax=docker/dockerfile:1.4
FROM python:3.7-alpine AS builder

WORKDIR /app

# On installe les dépendances dans l'image
COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

# On ne copie PLUS le code ici pour le dev, 
# car le volume va l'écraser de toute façon.
EXPOSE 8000

# Commande par défaut
CMD ["python3", "app/manage.py", "runserver", "0.0.0.0:8000"]