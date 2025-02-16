from fastapi import FastAPI, Query, HTTPException
import os
import json
import shutil
from datetime import datetime
import requests
from PIL import Image
import sqlite3

app = FastAPI()

# Ensure DATA_DIR exists (Update this path as per your setup)
DATA_DIR = os.getenv("DATA_DIR", os.path.expanduser("~/Desktop/data"))
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Welcome to the Automation Agent API"}

# 1️⃣ Extract sender email
@app.post("/run")
def run_task(task: str):
    task_map = {
        "extract sender email": extract_email,
        "count Wednesdays": count_wednesdays,
        "sort contacts": sort_contacts,
        "extract logs": extract_logs,
        "convert markdown to html": convert_markdown_to_html,
        "fetch data from API": fetch_api_data,
        "SQL query gold ticket sales": run_sql_query,
        "compress image": compress_image,
        "transcribe audio": transcribe_audio,
    }

    if task in task_map:
        return task_map[task]()

    return {"status": "error", "message": "Task not recognized"}

# 2️⃣ Read a file from the /data directory
@app.get("/read")
def read_file(filename: str):
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return {"status": "success", "content": content}

# 🔹 Extract sender email
def extract_email():
    file_path = os.path.join(DATA_DIR, "email.txt")
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    with open(file_path, "r") as file:
        email = file.readline().strip()

    with open(os.path.join(DATA_DIR, "email-sender.txt"), "w") as out_file:
        out_file.write(email)

    return {"status": "success", "message": "Email extracted"}

# 🔹 Count Wednesdays in a file
def count_wednesdays():
    file_path = os.path.join(DATA_DIR, "dates.txt")
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    count = 0
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    date_obj = datetime.strptime(line.strip(), "%Y-%m-%d")
                    if date_obj.weekday() == 2:
                        count += 1
                except ValueError:
                    continue
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success", "count": count}

# 🔹 Sort contacts alphabetically
def sort_contacts():
    file_path = os.path.join(DATA_DIR, "contacts.json")
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    with open(file_path, "r") as file:
        contacts = json.load(file)

    sorted_contacts = sorted(contacts, key=lambda x: x.get("name", ""))
    sorted_file = os.path.join(DATA_DIR, "contacts-sorted.json")

    with open(sorted_file, "w") as out_file:
        json.dump(sorted_contacts, out_file)

    return {"status": "success", "message": "Contacts sorted"}

# 🔹 Extract logs from logs folder
def extract_logs():
    logs_dir = os.path.join(DATA_DIR, "logs")
    if not os.path.exists(logs_dir):
        return {"status": "error", "message": "Logs directory not found"}

    log_files = sorted(os.listdir(logs_dir))[-1:]  # Get latest log file
    if not log_files:
        return {"status": "error", "message": "No logs available"}

    log_path = os.path.join(logs_dir, log_files[0])
    with open(log_path, "r") as file:
        logs = file.readlines()[-10:]  # Last 10 logs

    with open(os.path.join(DATA_DIR, "logs-recent.txt"), "w") as out_file:
        out_file.writelines(logs)

    return {"status": "success", "message": "Logs extracted"}

# 🔹 Convert Markdown to HTML
def convert_markdown_to_html():
    input_file = os.path.join(DATA_DIR, "format.md")
    output_file = os.path.join(DATA_DIR, "converted.html")

    if not os.path.exists(input_file):
        return {"status": "error", "message": "File not found"}

    with open(input_file, "r") as file:
        markdown_text = file.read()

    html_text = f"<html><body>{markdown_text.replace(chr(10), '<br>')}</body></html>"

    with open(output_file, "w") as out_file:
        out_file.write(html_text)

    return {"status": "success", "message": "Markdown converted to HTML"}

# 🔹 Fetch data from API
def fetch_api_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    if response.status_code == 200:
        with open(os.path.join(DATA_DIR, "api_data.json"), "w") as file:
            json.dump(response.json(), file)
        return {"status": "success", "message": "API data saved"}

    return {"status": "error", "message": "API request failed"}

# 🔹 SQL Query for Gold Ticket Sales
def run_sql_query():
    db_path = os.path.join(DATA_DIR, "ticket-sales.db")
    if not os.path.exists(db_path):
        return {"status": "error", "message": "Database not found"}

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales WHERE ticket_type = 'Gold'")
        result = cursor.fetchone()[0]
        conn.close()
        return {"status": "success", "gold_ticket_sales": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🔹 Compress an image
def compress_image():
    input_image = os.path.join(DATA_DIR, "credit_card.png")
    output_image = os.path.join(DATA_DIR, "compressed_credit_card.png")

    if not os.path.exists(input_image):
        return {"status": "error", "message": "File not found"}

    img = Image.open(input_image)
    img.save(output_image, "PNG", optimize=True, quality=20)

    return {"status": "success", "message": "Image compressed"}

# 🔹 Transcribe an audio file (Dummy Function)
def transcribe_audio():
    return {"status": "error", "message": "Transcription not implemented"}