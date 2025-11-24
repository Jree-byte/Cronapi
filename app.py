from flask import Flask, render_template_string
import pymysql
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # MySQL-yhteys
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='VITTU',
            password='Moimoi33-',
            database='weather'
        )
        cursor = conn.cursor()

        # Hae viimeisin säätieto
        cursor.execute("""
            SELECT city, temperature, description, timestamp
            FROM weather_data
            ORDER BY id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            message = f"{row[0]}: {row[1]}°C, {row[2]}"
            current_time = row[3]
        else:
            message = "No weather data available."
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.close()
        conn.close()

    except Exception as e:
        message = f"Database error: {e}"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LEMP Home</title>
        <style>
            body {{
                background-color: #eef4fa;
                font-family: Arial, sans-serif;
                text-align: center;
                color: #2c3e50;
                padding-top: 60px;
            }}
            .box {{
                background-color: #ffffff;
                display: inline-block;
                padding: 30px 50px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            h1 {{ color: #1a5276; }}
            p {{ font-size: 18px; }}
            a {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #1a5276;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            a:hover {{ background-color: #154360; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Welcome to LEMP Home</h1>
            <p>{message}</p>
            <p>Timestamp: {current_time}</p>
            <p><a href="http://127.0.0.1:8501" target="_blank">Go to Data Analysis (Streamlit)</a></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

