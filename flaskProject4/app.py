from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'pavan'
}
def get_db_connection():
    return mysql.connector.connect(**db_config)
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
def create_user_details_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS user_details1 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT,
                age INT,
                email TEXT NOT NULL,
                phone_number TEXT,
                qualification TEXT,
                address TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()
create_users_table()
create_user_details_table()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('details'))
    except mysql.connector.Error as e:
        return "Error inserting data into database: {}".format(str(e))

@app.route('/details', methods=['GET'])
def details():
    return render_template('details.html')
@app.route('/submit_details', methods=['POST'])
def submit_details():
    fname = request.form['firstName']
    lname = request.form['lastName']
    gender = request.form['gender']
    age = request.form['age']
    email = request.form['email']
    ph = request.form['phoneNumber']
    qua = request.form['qualification']
    addr = request.form['address']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get the ID of the last inserted user
        cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO user_details1 (user_id, first_name, last_name, gender, age, email, phone_number, qualification, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, fname, lname, gender, age, email, ph, qua, addr))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('user_details'))
    except mysql.connector.Error as e:
        return "Error inserting data into database: {}".format(str(e))
import logging
logging.basicConfig(level=logging.DEBUG)
@app.route('/user_details', methods=['GET'])
def user_details():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_details1")
        user_details = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.debug("Fetched user details: %s", user_details)
        return render_template('user_details.html', user_details=user_details)
    except mysql.connector.Error as e:
        logging.error("Error fetching data from database: %s", e)  # Add logging statement
        return "Error fetching data from database: {}".format(str(e))


if __name__ == '__main__':
    app.run(debug=True)
