# שלב הבסיס
FROM python:3.9-slim AS base

# התקנות מערכת
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

# יצירת תיקייה לאפליקציה
WORKDIR /app

# העתקת הדרישות והתקנת תלויות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקוד של האפליקציה
COPY . .

# פתיחת פורט 5000
EXPOSE 5000

# הרצת האפליקציה
CMD ["python", "app.py"]

