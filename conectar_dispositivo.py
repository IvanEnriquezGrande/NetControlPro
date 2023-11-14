from netmiko import ConnectHandler
from database import conectar_db

def insertar_tipo_dispositivo(dispositivo):
    mydb = conectar_db()
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

def obtener_tipo_dispositivo(dispositivo):
    
    output = dispositivo.send_command('show vlan brief')
    print(output)
    
    if "Invalid input detected" in output:
        return "router"
    else:
        return "switch"
    
#@app.route('/conexion-switch', methods=["GET", "POST"])
def conexion_switch(ip, username, password):
    switch = {
        'ip': ip,
        'username': username,
        'passsword': password,
        'device_type': 'cisco_ios',
    }

    conexion = ConnectHandler(**switch)
    tipo_dispositivo = obtener_tipo_dispositivo(conexion)
    insertar_tipo_dispositivo(tipo_dispositivo)

    return 0

