# 1. Python Image
FROM python:3.13-slim

# 2. app folder
WORKDIR /app

# 3. Copy just requirements for optimazation
COPY requirements.txt .

# 4. Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy
COPY . .

# 6. Initialization
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]