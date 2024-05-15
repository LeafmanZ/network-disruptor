# README for Network Resilience Evaluation Tool

## Overview

This tool is designed to evaluate network resilience by simulating various network conditions on a portable device. It utilizes a Raspberry Pi to emulate network disruptions such as latency, jitter, packet loss, and bandwidth constraints. The device is equipped with a user-friendly touchscreen interface, making it accessible for users with varying levels of technical expertise.

## System Design

The interface of the tool is a web application developed using HTML and JavaScript for the front end, and Python Flask for the back end. The network disruption functionalities are achieved using a Linux library called “brctl”. Flask interacts with this library, allowing users to manage network settings directly through the web interface.

## Device Setup

1. **Install OS:** Install the 64-bit Raspberry Pi OS on your Raspberry Pi.
2. **Install Touchscreen:** Connect the official 7-inch Raspberry Pi touchscreen to your device.
3. **Download Source Code:** Use the following command in the terminal to clone the repository:
    ```bash
    git clone https://github.com/LeafmanZ/network-disruptor.git
    ```
    Alternatively, download and extract the 'network-disruptor' folder containing the source code.
4. **Install bridge-utils:** Install the `bridge-utils` package to manage network bridges:
    ```bash
    sudo apt install bridge-utils
    ```
5. **System Update and Upgrade:** Run the following commands in the terminal to update and upgrade your system:
    ```bash
    sudo apt update && sudo apt upgrade
    ```
6. **Install Pip:** Before installing Flask, ensure that `pip` is installed:
    ```bash
    sudo apt install python3-pip
    ```
7. **Install Flask:** Now, install Flask using `pip`:
    ```bash
    pip install flask
    ```
8. **Configure Startup Commands:**
    Open your cron table for editing by running:
    ```bash
    crontab -e
    ```
    Add the following lines at the end of the cron table, ensuring that you adjust the paths to match the location where the 'disrupt_app' folder is stored:
    ```cron
    @reboot sudo python /home/<username>/Desktop/disrupt_app/app.py
    @reboot bash /home/<username>/Desktop/disrupt_app/launch_chromium.sh
    ```
9. **Reboot Device:** Restart your Raspberry Pi to apply the changes:
    ```bash
    sudo reboot
    ```
10. **Verify Setup:** Upon reboot, you should see the menu appear on the screen.
11. **Connect Ethernet Adapters:** Plug in two USB-to-Ethernet adapters into your Raspberry Pi. You should then see the status checks for `eth1` and `eth2` resolve.

## Operation

### Initial Setup

1. **Power On:** Turn on the Raspberry Pi device which is equipped with a touchscreen.
2. **Connect Adapters:** Attach two USB-to-Ethernet adapters to the Raspberry Pi.
3. **Adapter Recognition:** Upon connection, the interface will recognize the Ethernet adapters and display their status. Flask then automatically configures a bridge between the two Ethernet ports using “brctl”.

### Integration into Network

1. **Disconnect Existing Connection:** Remove an Ethernet cable from its original socket and connect it to one of the Raspberry Pi’s Ethernet ports.
2. **Establish New Connection:** Connect another Ethernet cable to the second Raspberry Pi port and plug it back into the original socket from which the first cable was disconnected.

This configuration allows network traffic to pass through the Raspberry Pi as if it were part of the network seamlessly.

### Network Manipulation

Through the touchscreen interface, users can manipulate sliders to adjust:
- **Latency**
- **Jitter**
- **Packet Loss**
- **Bandwidth Constraints**

These settings enable users to stress-test the network’s robustness under various conditions, assessing the network's resilience effectively.

## Conclusion

This tool provides a practical and efficient method for simulating network conditions and testing network resilience, suitable for use in diverse environments and applications.