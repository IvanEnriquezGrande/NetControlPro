from flask import Flask, render_template, request, redirect, url_for
from conectar_dispositivo import conexion_equipo
from database import conectar_db

app = Flask(__name__)

@app.route("/add", methods=['POST'])
def add():
    # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        deviceIp = request.form['deviceIp']
        deviceName = request.form['deviceName']
        deviceUsername = request.form['deviceUsername']
        devicePassword = request.form['devicePassword']

        deviceType = conexion_equipo(deviceIp, deviceUsername, devicePassword)

        query = f"INSERT INTO devices (device_ip, device_name, device_username, device_password, device_type) VALUES (%s, %s, %s, %s, %s)"
        data = (deviceIp, deviceName, deviceUsername, devicePassword, deviceType)

        cursor.execute(query, data)
        conexion.commit()

        return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True) 

    query = f"DELETE FROM devices WHERE device_id=%s"
    data = (id,)

    cursor.execute(query, data)
    conexion.commit()

    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['POST'])
def edit(id):

    deviceIp = request.form['deviceIp']
    deviceName = request.form['deviceName']
    deviceUsername = request.form['deviceUsername']
    devicePassword = request.form['devicePassword']
    
    # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    query = f"UPDATE devices SET device_ip=%s, device_name=%s, device_username=%s, device_password=%s WHERE device_id=%s"
    data = (deviceIp, deviceName, deviceUsername, devicePassword, id)

    cursor.execute(query, data) 
    conexion.commit()

    return redirect(url_for('index'))

#MUESTRA SOLO LOS ROUTERS    
@app.route('/routers')
def routers():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices WHERE device_type = 'router'")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

#MUESTRA SOLO LOS SWITCHES
@app.route('/switches')
def switches():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices WHERE device_type = 'switch'")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

#MUESTRA TODOS LOS DISPOSITIVOS
@app.route("/all_devices")
def all_devices():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

#ORDENA POR NOMBRE   
@app.route('/order_name')
def order_name():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices ORDER BY device_name")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

#ORDENA POR FECHA   
@app.route('/order_date')
def order_date():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices ORDER BY add_date")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

@app.route("/")
def index():
     # Conectarse a la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conexion.close()

    return render_template('index.html', devices=devices)

# Route for switch configuration
@app.route("/switch-config/<device_id>")
def switch_config(device_id):
    return render_template('switch-config.html', switch_id=device_id)

# Route for router configuration
@app.route("/router-config/<device_id>")
def router_config(device_id):
    return render_template('router-config.html', router_id=device_id)

if __name__ == '__main__':
    app.run(debug=True, port=8000)