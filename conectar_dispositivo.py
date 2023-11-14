from netmiko import ConnectHandler

#Method that connnects to a specific device
def device_connection(ip, username, password):
    switch = {
        'host': ip,
        'username': username,
        'password': password,
        'secret': password,
        'device_type': 'cisco_ios',
        'read_timeout_override': 90
    }
    conexion = ConnectHandler(**switch)
    return conexion

def device_type(dispositivo):
    output = dispositivo.send_command('show vlan brief')
    print(output)
    
    if "Invalid input detected" in output:
        return "router"
    else:
        return "switch"
    
def get_device_type(ip, username, password):
    switch = {
        'host': ip,
        'username': username,
        'password': password,
        'device_type': 'cisco_ios',
    }

    conexion = ConnectHandler(**switch)
    tipo_dispositivo = device_type(conexion)
    return tipo_dispositivo


def get_device_vlans(equipo):
    raw_vlans = equipo.send_command('show vlan brief')
    return raw_vlans

def modify_stp_value(device, vlan, value):
    commands = [f'spanning-tree vlan {vlan} priority {value}']
    device.enable()
    output = device.send_config_set(commands)
    return output

def activate_cdp(device):
    commands = ['cdp run']
    device.enable()
    output = device.send_config_set(commands)
    return output

def disable_cdp(device):
    commands = ['no cdp run']
    device.enable()
    output = device.send_config_set(commands)
    return output

def activate_root_bridge(device, vlan, root):
    commands = [f'spanning-tree vlan {vlan} root {root}']
    device.enable()
    device.send_config_set(commands)
