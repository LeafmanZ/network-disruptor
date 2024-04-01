import subprocess

def execute_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")

commands = [
    "sudo ifconfig eth1 up",
    "sudo ifconfig eth2 up",
    "sudo ip link add br0 type bridge",
    "sudo ip link set br0 up",
    "sudo ip link set dev eth1 master br0",
    "sudo ip link set dev eth2 master br0",
    "sudo dhclient br0",
    "sudo brctl show",
    "sudo brctl addif br0 eth1",
    "sudo brctl addif br0 eth2",
    "sudo echo 1 > /proc/sys/net/ipv4/ip_forward",
    "sudo ip addr add 10.20.10.7/24 dev br0"
]

for cmd in commands:
    execute_command(cmd)
