from flask import Flask, render_template, request, redirect, url_for
import pymysql
import requests
from db_config import get_db_connection

app = Flask(__name__)

def get_az():
    try:
        return requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone', timeout=1).text
    except:
        return "Unavailable"

@app.route('/')
def index():
    az = get_az()
    return render_template('index.html', az=az)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO submissions (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
    conn.close()
    return redirect(url_for('data'))

@app.route('/data')
def data():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM submissions")
        data = cursor.fetchall()
    conn.close()
    az = get_az()
    return render_template('data.html', submissions=data, az=az)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
