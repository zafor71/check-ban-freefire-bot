FROM python:3.9-slim

# Copier les fichiers de ton projet
WORKDIR /app
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exécution du script Python
CMD ["python", "main.py"]
