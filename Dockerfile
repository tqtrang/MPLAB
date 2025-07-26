# Use official Python 3.11 image
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the rest of the app
COPY . /app/
# ✅ Ép copy đúng file DB
COPY db/my_data.db /app/db/my_data.db

# Command to run the app (tùy bạn dùng Flask hay Streamlit)
CMD ["python", "app.py"]
