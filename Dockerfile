# Imatge base lleugera de Python
FROM python:3.11-slim

# Crear directori de treball
WORKDIR /app

# Copiar fitxers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposar port
EXPOSE 8000

# Comanda d'arrencada
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
