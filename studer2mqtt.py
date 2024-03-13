import serial
from xcom485i.client import Xcom485i
import paho.mqtt.client as mqtt

SERIAL_PORT_NAME = '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0-port0'  # your serial port interface name
SERIAL_PORT_BAUDRATE = 115200  # baudrate used by your serial interface
DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device

# MQTT broker configuration
MQTT_BROKER = 'net.ad.kolins.cz'
MQTT_PORT = 1883  # Default MQTT port
MQTT_TOPIC = 'studer'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

if __name__ == "__main__":
    try:
        serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE, parity=serial.PARITY_EVEN, timeout=1)
    except serial.serialutil.SerialException as e:
        print("Check your serial configuration:", e)
    else:
        xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=False)
        # MQTT client setup
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        #client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()

        while True:
            l1_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_l1_group_device_id, 278)
            l1_active_power = xcom485i.read_info(xcom485i.addresses.xt_l1_group_device_id, 272)
            l1_apparent_power = round(l1_apparent_power, 3)
            l1_active_power = round(l1_active_power, 3)
            print('L1 power:', l1_apparent_power, 'kVA', '   ', l1_active_power, 'kW')

            l2_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_l2_group_device_id, 278)
            l2_active_power = xcom485i.read_info(xcom485i.addresses.xt_l2_group_device_id, 272)
            l2_apparent_power = round(l2_apparent_power, 3)
            l2_active_power = round(l2_active_power, 3)
            print('L2 power:', l2_apparent_power, 'kVA', '   ', l2_active_power, 'kW')

            l3_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_l3_group_device_id, 278)
            l3_active_power = xcom485i.read_info(xcom485i.addresses.xt_l3_group_device_id, 272)
            l3_apparent_power = round(l3_apparent_power, 3)
            l3_active_power = round(l3_active_power, 3)
            print('L3 power:', l3_apparent_power, 'kVA', '   ', l3_active_power, 'kW')

            outputfreq = xcom485i.read_info(xcom485i.addresses.xt_group_device_id, 170)
            outputfreq = round(outputfreq, 3)
            print('Output frequency:', outputfreq, 'Hz')
            
            client.publish(f"{MQTT_TOPIC}/L1_apparent_power", f"{l1_apparent_power} kVA")
            client.publish(f"{MQTT_TOPIC}/L1_active_power", f"{l1_active_power} kW")
            client.publish(f"{MQTT_TOPIC}/L2_apparent_power", f"{l2_apparent_power} kVA")
            client.publish(f"{MQTT_TOPIC}/L2_active_power", f"{l2_active_power} kW")
            client.publish(f"{MQTT_TOPIC}/L3_apparent_power", f"{l3_apparent_power} kVA")
            client.publish(f"{MQTT_TOPIC}/L3_active_power", f"{l3_active_power} kW")
            client.publish(f"{MQTT_TOPIC}/Output_frequency", f"{outputfreq} Hz")
