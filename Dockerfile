# 1️⃣ Use Python 3.11 as the base image
FROM python:3.11

# 2️⃣ Create a directory in the container for the app
WORKDIR /app

# 3️⃣ Copy all files from your local project folder to the container
COPY . /app

# 4️⃣ Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Environment variables (optional)
ENV DATA_DIR="/data"

# 6️⃣ Expose port 8000 for FastAPI
EXPOSE 8000

# 7️⃣ Default command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

