from netmiko import ConnectHandler

def parseo_vlans(ip, username, password):
    switch = {
        'ip': ip,
        'username': username,
        'passsword': password,
        'device_type': 'cisco_ios',
    }

    vlans = {}

    conexion = ConnectHandler(**switch)
    get_vlans = conexion.send_command("show vlans")

    for linea in get_vlans.split('\n'):
        palabras = linea.split()

        if palabras[0].isdigit():
            vlans[int(palabras[0])] = palabras[1]
    
    return vlans
