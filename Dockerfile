# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application using uvicorn
CMD ["poetry", "run", "uvicorn", "src.ui.app:app", "--host", "0.0.0.0", "--port", "8000"]