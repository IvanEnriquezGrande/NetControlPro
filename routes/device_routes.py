from flask import render_template, request, redirect, url_for, flash, session
from conectar_dispositivo import *
from database import conectar_db, DatabaseConnectionError

def connect_device(device_id):
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

        current_device = device_connection(ip, username, password)
        session['current_device'] = current_device
    except DatabaseConnectionError as e:
        pass
    except Exception as e:
        pass
    return redirect(url_for('switch_config', device_id=device_id))

# Route for switch configuration
def switch_config(device_id):
    try:
        current_device = session.get('current_device')
        # VLANs RAW Output we need to parse and show in the switch-config.html
        raw_vlans = get_device_vlans(current_device)
        print(raw_vlans)

        # disable_cdp(current_device)
        # activate_cdp(current_device)
        # activate_root_bridge(current_device, 1, 'primary')
    except DatabaseConnectionError as e:
        pass
    except:
        pass
    return render_template('switch-config.html', switch_id=device_id)

def update_switch_state():
    try:
        current_device = session.get('current_device')
        if current_device is None:
            return {'status': 'error', 'message': 'Current device not found in the session'}
        
        data = request.get_json()
        switch_type = data.get('switchType')
        switch_state = data.get('switchState')
        print(switch_type)
        if switch_type == 'cdp':
            if switch_state:
                activate_cdp(current_device)
            else:
                disable_cdp(current_device)
    except DatabaseConnectionError as e:
        pass
    except:
        pass

    return {'status': 'success'}

# Route for router configuration
def router_config(device_id):
    return render_template('router-config.html', router_id=device_id)
