from flask import Flask, render_template, request, jsonify
import json
import subprocess
import re
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_metrics', methods=['POST'])
def submit_metrics():
    data = request.json
    active_metrics = data.get('activeMetrics', {})
    print("Received Metrics:")
    for key, value in active_metrics.items():
        print(f"{key}: {value}")

    # Save to disk
    with open('metrics_data.json', 'w') as file:
        json.dump(active_metrics, file)

    ens192_reset_cmd = ["sudo", "tc", "qdisc", "del", "dev", "ens192", "root"]
    ens192_cmd = ["sudo", "tc", "qdisc", "add", "dev", "ens192", "root", "netem", "rate", f"{active_metrics['ens192-slider-bandwidth']}mbit", "loss", f"{active_metrics['ens192-slider-packet-loss']}%", "corrupt", f"{active_metrics['ens192-slider-packet-corruption']}%", "delay", f"{active_metrics['ens192-slider-base-latency']}ms", f"{active_metrics['ens192-slider-latency-jitter']}ms", "25%"]
    
    ens224_reset_cmd = ["sudo", "tc", "qdisc", "del", "dev", "ens224", "root"]
    ens224_cmd = ["sudo", "tc", "qdisc", "add", "dev", "ens224", "root", "netem", "rate", f"{active_metrics['ens224-slider-bandwidth']}mbit", "loss", f"{active_metrics['ens224-slider-packet-loss']}%", "corrupt", f"{active_metrics['ens224-slider-packet-corruption']}%", "delay", f"{active_metrics['ens224-slider-base-latency']}ms", f"{active_metrics['ens224-slider-latency-jitter']}ms", "25%"]

    # Running the commands
    subprocess.run(ens192_reset_cmd, check=True)
    subprocess.run(ens192_cmd, check=True)
    subprocess.run(ens224_reset_cmd, check=True)
    subprocess.run(ens224_cmd, check=True)

    # Return the same data for frontend
    return jsonify(active_metrics)

@app.route('/save_default', methods=['POST'])
def save_default():
    data = request.json
    default_metrics = data.get('defaultMetrics', {})
    print("Saving Default Metrics:")
    for key, value in default_metrics.items():
        print(f"{key}: {value}")

    # Save to disk
    with open('default_data.json', 'w') as file:
        json.dump(default_metrics, file)

    return jsonify({"message": "Default metrics saved successfully"})

@app.route('/get_metrics_data', methods=['GET'])
def get_metrics_data():
    try:
        with open('metrics_data.json', 'r') as file:
            metrics_data = json.load(file)
            return jsonify(metrics_data)
    except FileNotFoundError:
        return jsonify({"error": "Metrics data not found"}), 404

@app.route('/get_default_metrics', methods=['GET'])
def get_default_metrics():
    try:
        with open('default_data.json', 'r') as file:
            default_metrics = json.load(file)
            return jsonify(default_metrics)
    except FileNotFoundError:
        return jsonify({"error": "Default metrics not found"}), 404

@app.route('/network-status')
def network_status():
    # Run the ifconfig command and capture its output
    result = subprocess.run(['sudo', 'ifconfig'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # Function to check the connection status of a network interface
    def check_connection(interface):
        # Use regular expressions to check if the interface is mentioned in the output
        if re.search(f'^{interface}:', output, re.MULTILINE):
            return "connected"
        else:
            return "not connected"

    # Check the status of ens192 and ens224
    ens192_status = check_connection('ens192')
    ens224_status = check_connection('ens224')

    # Return the status as a JSON response
    return jsonify({"ens192": ens192_status, "ens224": ens224_status})

def execute_command(command):
    try:
        # Adjusted to directly execute without shell=True where feasible
        subprocess.run(["sudo"] + command.split(), check=True)
        print(f"Executed: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(command)}: {e}")

def check_interface_exists(interface):
    result = subprocess.run(["sudo", "ifconfig", interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def check_bridge_contains_interfaces():
    result = subprocess.run(["sudo", "brctl", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode()
    return 'ens192' in output and 'ens224' in output

@app.route('/reticulating_spines')
def reticulating_spines():
    if check_bridge_contains_interfaces():
        print("skipping")
        return jsonify({"status": "ens192 and ens224 already in bridge, skipping"})

    commands = [
        "ifconfig ens192 up",
        "ifconfig ens224 up",
    ]

    if not check_interface_exists("br0"):
        commands.extend([
            "ip link add br0 type bridge",
            "ip link set br0 up",
            "ip link set dev ens192 master br0",
            "ip link set dev ens224 master br0"
        ])

    commands.extend([
            "brctl addif br0 ens192",
            "brctl addif br0 ens224"
        ])

    for cmd in commands:
        execute_command(cmd)

    time.sleep(5)  # Simulate a delay
    return jsonify({"status": "completed"})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port="5000")
