from flask import render_template, request, redirect, url_for, flash
from conectar_dispositivo import *
from database import conectar_db, DatabaseConnectionError

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
