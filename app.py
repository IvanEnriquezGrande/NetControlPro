from flask import Flask
from routes.main_routes import add, edit, delete, index, routers, switches, all_devices, order_name, order_date
from routes.device_routes import connect_device, switch_config, update_switch_state, router_config

app = Flask(__name__)

app.secret_key = "your_secret_key"

# Main routes
app.route("/add", methods=['POST'])(add)
app.route('/delete/<id>')(delete)
app.route('/edit/<id>', methods=['POST'])(edit)
app.route('/routers')(routers)
app.route('/switches')(switches)
app.route("/all_devices")(all_devices)
app.route('/order_name')(order_name)
app.route('/order_date')(order_date)
app.route("/")(index)

# Device routes
app.route('/connect-device/<device_id>')(connect_device)
app.route("/switch-config/<device_id>")(switch_config)
app.route('/update-switch-state', methods=['POST'])(update_switch_state)
app.route("/router-config/<device_id>")(router_config)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
