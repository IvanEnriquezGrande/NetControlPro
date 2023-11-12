from flask import Flask, render_template, request, redirect, url_for, flash
from conectar_dispositivo import *
from database import conectar_db, DatabaseConnectionError

app = Flask(__name__)

app.secret_key = "your_secret_key"

@app.route("/add", methods=['POST'])
def add():
    try:
    # Conectarse a la base de datos
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)
        
        if request.method == 'POST':
            deviceIp = request.form['deviceIp']
            deviceName = request.form['deviceName']
            deviceUsername = request.form['deviceUsername']
            devicePassword = request.form['devicePassword']

            deviceType = get_device_type(deviceIp, deviceUsername, devicePassword)

            query = f"INSERT INTO devices (device_ip, device_name, device_username, device_password, device_type, add_date) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)"
            data = (deviceIp, deviceName, deviceUsername, devicePassword, deviceType)

            cursor.execute(query, data)
            conexion.commit()

            flash("El dispositivo se agregó correctamente")
            return redirect(url_for('index'))
    except DatabaseConnectionError as e:
        flash(str(e))
        return render_template('index.html', devices={})
    except Exception as e:
        flash("Error: La conexión TCP al dispositivo ha fallado. Las posibles causan son: 1. Nombre de host o dirección ip incorrectas. 2. Puerto TCP equivocado. Configuración de dispositivo: " + deviceIp)
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

    flash("El dispositivo se ha eliminado")
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

    flash("Los datos del dispositivo se actualizaron correctamente")
    return redirect(url_for('index'))

#MUESTRA SOLO LOS ROUTERS    
@app.route('/routers')
def routers():
    try:
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
    except DatabaseConnectionError as e:
        flash(str(e))
    return render_template('index.html', devices={})

#MUESTRA SOLO LOS SWITCHES
@app.route('/switches')
def switches():
    try:
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
    except DatabaseConnectionError as e:
        flash(str(e))
    return render_template('index.html', devices={})

#MUESTRA TODOS LOS DISPOSITIVOS
@app.route("/all_devices")
def all_devices():
    try:
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
    except DatabaseConnectionError as e:
        flash(str(e))
    return render_template('index.html', devices={})

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
    try:
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
    except DatabaseConnectionError as e:
        flash(str(e))
    return render_template('index.html', devices={})

# Route for switch configuration
@app.route("/switch-config/<device_id>")
def switch_config(device_id):
    try:
        #Connection to database
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)

        #Retrieve the device information
        query = f"SELECT device_ip, device_username, device_password FROM devices WHERE device_id = %s"
        data = [device_id]
        cursor.execute(query,data)
        device_info = cursor.fetchall()

        ip = device_info[0].get('device_ip')
        username = device_info[0].get('device_username')
        password = device_info[0].get('device_password')

        
        #Connection to specific device
        device = device_connection(ip, username, password)
        
        #VLANs RAW Output we need to parse and show in the switch-config.html
        raw_vlans = get_device_vlans(device)
        print(raw_vlans)

        disable_cdp(device)
        activate_cdp(device)
        activate_root_bridge_primaty(device)
        

    except DatabaseConnectionError as e:
        pass
    return render_template('switch-config.html', switch_id=id)

# Route for router configuration
@app.route("/router-config/<device_id>")
def router_config(device_id):
    return render_template('router-config.html', router_id=device_id)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
