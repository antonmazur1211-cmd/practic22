FROM python:3.13-slim

WORKDIR /app

# Встановлення Poetry
RUN pip install poetry

# Копіювання файлів залежностей
COPY pyproject.toml ./

# Встановлення залежностей без створення віртуального середовища
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Копіювання коду проекту
COPY . .

# Команда для запуску з автоперезагрузкою
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
