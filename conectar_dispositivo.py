from netmiko import ConnectHandler
import mysql.connector

def insertar_tipo_dispositivo(dispositivo):

    mydb = mysql.connector.connect(
        user = 'root',
        password = 'root',
        host='127.0.0.1', 
        port=3306,
        database='devices'
    )

    cursor = mydb.cursor()

    cursor.execute("INSERT INTO devices (device_type) VALUES (dispositivo);")
    mydb.commit()
    mydb.close()

def obtener_tipo_disp(dispositivo):
    datos_dispositivo = dispositivo.get_facts()

    if 'vlan_list' in datos_dispositivo:
        return 'switch'
    else:
        return 'router'

#@app.route('/conexion-switch', methods=["GET", "POST"])
def conexion_switch(ip, username, password):
    switch = {
        'ip': ip,
        'username': username,
        'passsword': password,
        'device_type': 'cisco_ios',
    }

    conexion = ConnectHandler(**switch)
    tipo_dispositivo = obtener_tipo_disp(conexion)
    insertar_tipo_dispositivo(tipo_dispositivo)

    return 0

#@app.route('/conexion-router', methods=["GET", "POST"])
def conexion_router(ip, username, password):
    router = {
        'ip': ip,
        'username': username,
        'passsword': password,
        'device_type': 'cisco_ios',
    }

    conexion = ConnectHandler(**router)
    tipo_dispositivo = obtener_tipo_disp(conexion)
    insertar_tipo_dispositivo(tipo_dispositivo)

    return 0
