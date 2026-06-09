# Используем официальный образ Python как базовый
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock ./

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем Poetry
RUN pip install poetry

# Отключаем создание нового виртуального окружения
RUN poetry config virtualenvs.create false

# Устанавливаем только зависимости
RUN poetry install --no-root

# Копируем остальной код приложения
COPY . .

# Указываем порт, на котором будет работать Django (по умолчанию 8000)
EXPOSE 8000

# Команда для запуска Django-сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

#FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
