from flask import Blueprint, render_template, jsonify
import mysql.connector
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route("/drivers")
def get_drivers():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1420',
        database='f1db'
    )
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        CONCAT(d.first_name, ' ', d.last_name) AS driver_name,
        d.nationality,
        SUM(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS total_wins,
        ROUND(SUM(r.points), 1) AS career_points,
        GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS teams
        
    FROM drivers d
    JOIN results r ON d.driver_id = r.driver_id
    JOIN constructors c ON r.constructor_id = c.constructor_id
    GROUP BY d.driver_id
    ORDER BY career_points DESC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)
