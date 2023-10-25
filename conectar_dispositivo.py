from netmiko import ConnectHandler
#from app import conectar_db
import mysql.connector

"""
def insertar_tipo_dispositivo(dispositivo):
    mydb = conectar_db()
    cursor = mydb.cursor()

    cursor.execute("INSERT INTO devices (device_type) VALUES (dispositivo);")
    mydb.commit()
    mydb.close()
"""
    
def obtener_tipo_disp(dispositivo):
    datos_dispositivo = dispositivo.get_facts()

    if 'vlan_list' in datos_dispositivo:
        return 'switch'
    else:
        return 'router'

def obtener_tipo_dispositivo(dispositivo):
    output = dispositivo.send_command('show vlan brief')
    print(output)
    
    if "Invalid input detected" in output:
        return "router"
    else:
        return "switch"
    
"""        
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
"""
    
def conexion_equipo(ip, username, password):
    switch = {
        'host': ip,
        'username': username,
        'password': password,
        'device_type': 'cisco_ios',
    }

    conexion = ConnectHandler(**switch)
    tipo_dispositivo = obtener_tipo_dispositivo(conexion)
    print(tipo_dispositivo)
    return tipo_dispositivo