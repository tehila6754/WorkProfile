
# שלב הבסיס
FROM python:3.9-slim AS base

# התקנות מערכת
#RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# יצירת תיקייה לאפליקציה
WORKDIR /app

# העתקת הדרישות והתקנת תלויות
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org -r requirements.txt

# העתקת כל הקוד של האפליקציה
COPY . .

# פתיחת פורט 5000
EXPOSE 5000

# הרצת האפליקציה
CMD ["python", "app.py"]

