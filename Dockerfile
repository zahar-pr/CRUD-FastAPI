FROM python:3.10.12-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Скопируем зависимости и установим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Команда по умолчанию — запуск FastAPI сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]












