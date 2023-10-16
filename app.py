from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
app.config['DB_HOST'] = '127.0.0.1'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'root'
app.config['DB_DATABASE'] = 'devices'
app.config['DB_PORT'] = 3306  # Puerto MySQL predeterminado

# Función para conectar a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_DATABASE'],
        port=app.config['DB_PORT']  # Especificar el puerto aquí
    )

@app.route("/")
def index():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT device_id, device_name, device_ip, device_type FROM devices")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True, port=8000)