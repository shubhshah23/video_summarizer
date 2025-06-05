import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="vs",
    password="vs@123",
    database="videosummarizer"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM detections")
print(cursor.fetchall())