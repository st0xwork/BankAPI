FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "src/main/api/tests", "-m", "api", "--alluredir=/app/reports/allure"]
