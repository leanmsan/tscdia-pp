# Utiliza una imagen oficial de Python como base
FROM python:3.12-slim

# Instalar curl para healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos primero y los instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente del backend
COPY . .

# Expone el puerto en el que correrá FastAPI (por defecto 8000)
EXPOSE 8000

# Comando para iniciar el backend con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]