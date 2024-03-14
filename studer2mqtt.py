# https://xcom485i.readthedocs.io/en/latest/addresses.html

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

            l1_batt_current = xcom485i.read_info(xcom485i.addresses.xt_l1_group_device_id, 10)
            l1_batt_current  = round(l1_batt_current , 3)
            print('L1 Battery Current:', l1_batt_current , 'A')

            l2_batt_current = xcom485i.read_info(xcom485i.addresses.xt_l2_group_device_id, 10)
            l2_batt_current  = round(l2_batt_current , 3)
            print('L2 Battery Current:', l2_batt_current , 'A')

            l3_batt_current = xcom485i.read_info(xcom485i.addresses.xt_l3_group_device_id, 10)
            l3_batt_current  = round(l3_batt_current , 3)
            print('L3 Battery Current:', l3_batt_current , 'A')
            
            total_aparrent_power = xcom485i.read_info(xcom485i.addresses.xt_group_device_id, 278)
            total_active_power = xcom485i.read_info(xcom485i.addresses.xt_group_device_id, 272)
            total_aparrent_power = round(total_aparrent_power, 3)
            total_active_power = round(total_active_power, 3)
            print('Total power:', total_aparrent_power, 'kVA', '   ', total_active_power, 'kW')

            battery_voltage = xcom485i.read_info(xcom485i.addresses.xt_group_device_id, 0)
            battery_voltage = round(battery_voltage, 3)
            print('Battery voltage:', battery_voltage, 'V')

            battery_voltage_target = xcom485i.read_info(xcom485i.addresses.xt_group_device_id, 324)
            battery_voltage_target = round(battery_voltage_target, 3)
            print('Battery voltage target:', battery_voltage_target, 'V')


            sum_apparent_power = round(l1_apparent_power + l2_apparent_power + l3_apparent_power,3)
            sum_active_power = round(l1_active_power + l2_active_power + l3_active_power,3)
            print('Sum power:', sum_apparent_power, 'kVA', '   ', sum_active_power, 'kW')

            xt1_batt_current = xcom485i.read_info(xcom485i.addresses. xt_1_device_id, 10)
            xt1_batt_current  = round(xt1_batt_current , 3)
            print('XT1 Battery Current:', xt1_batt_current , 'A')

            xt2_batt_current = xcom485i.read_info(xcom485i.addresses. xt_2_device_id, 10)
            xt2_batt_current  = round(xt2_batt_current , 3)
            print('XT2 Battery Current:', xt2_batt_current , 'A')

            xt3_batt_current = xcom485i.read_info(xcom485i.addresses. xt_3_device_id, 10)
            xt3_batt_current  = round(xt3_batt_current , 3)
            print('XT3 Battery Current:', xt3_batt_current , 'A')

            xt4_batt_current = xcom485i.read_info(xcom485i.addresses. xt_4_device_id, 10)
            xt4_batt_current  = round(xt4_batt_current , 3)
            print('XT4 Battery Current:', xt4_batt_current , 'A')
            
            xt1_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, 278)
            xt1_active_power = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, 272)
            xt1_apparent_power = round(xt1_apparent_power, 3)
            xt1_active_power = round(xt1_active_power, 3)
            print('XT1 power:', xt1_apparent_power, 'kVA', '   ', xt1_active_power, 'kW')

            xt2_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_2_device_id, 278)
            xt2_active_power = xcom485i.read_info(xcom485i.addresses.xt_2_device_id, 272)
            xt2_apparent_power = round(xt2_apparent_power, 3)
            xt2_active_power = round(xt2_active_power, 3)
            print('XT2 power:', xt2_apparent_power, 'kVA', '   ', xt2_active_power, 'kW')

            xt3_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_3_device_id, 278)
            xt3_active_power = xcom485i.read_info(xcom485i.addresses.xt_3_device_id, 272)
            xt3_apparent_power = round(xt3_apparent_power, 3)
            xt3_active_power = round(xt3_active_power, 3)
            print('XT3 power:', xt3_apparent_power, 'kVA', '   ', xt3_active_power, 'kW')

            xt4_apparent_power = xcom485i.read_info(xcom485i.addresses.xt_4_device_id, 278)
            xt4_active_power = xcom485i.read_info(xcom485i.addresses.xt_4_device_id, 272)
            xt4_apparent_power = round(xt4_apparent_power, 3)
            xt4_active_power = round(xt4_active_power, 3)
            print('XT4 power:', xt4_apparent_power, 'kVA', '   ', xt4_active_power, 'kW')
            
            client.publish(f"{MQTT_TOPIC}/XT/XT1_apparent_power_kVA", str(xt1_apparent_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT1_active_power_kW", str(xt1_active_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT2_apparent_power_kVA", str(xt2_apparent_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT2_active_power_kW", str(xt2_active_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT3_apparent_power_kVA", str(xt3_apparent_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT3_active_power_kW", str(xt3_active_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT4_apparent_power_kVA", str(xt4_apparent_power))
            client.publish(f"{MQTT_TOPIC}/XT/XT4_active_power_kW", str(xt4_active_power))
            client.publish(f"{MQTT_TOPIC}/AC/L1_apparent_power_kVA", str(l1_apparent_power))
            client.publish(f"{MQTT_TOPIC}/AC/L1_active_power_kW", str(l1_active_power))
            client.publish(f"{MQTT_TOPIC}/AC/L2_apparent_power_kVA", str(l2_apparent_power))
            client.publish(f"{MQTT_TOPIC}/AC/L2_active_power_kW", str(l2_active_power))
            client.publish(f"{MQTT_TOPIC}/AC/L3_apparent_power_kVA", str(l3_apparent_power))
            client.publish(f"{MQTT_TOPIC}/AC/L3_active_power_kW", str(l3_active_power))
            client.publish(f"{MQTT_TOPIC}/AC/Output_frequency_Hz", str(outputfreq))
            client.publish(f"{MQTT_TOPIC}/AC/Total_apparent_power_kVA", str(total_aparrent_power))
            client.publish(f"{MQTT_TOPIC}/AC/Total_active_power_kW", str(total_active_power))
            client.publish(f"{MQTT_TOPIC}/DC/L1_Battery_Current_A", str(l1_batt_current))
            client.publish(f"{MQTT_TOPIC}/DC/L2_Battery_Current_A", str(l2_batt_current))
            client.publish(f"{MQTT_TOPIC}/DC/L3_Battery_Current_A", str(l3_batt_current))
            client.publish(f"{MQTT_TOPIC}/DC/Battery_voltage_V", str(battery_voltage))
            client.publish(f"{MQTT_TOPIC}/AC/Sum_apparent_power_kVA", str(sum_apparent_power))
            client.publish(f"{MQTT_TOPIC}/AC/Sum_active_power_kW", str(sum_active_power))
            client.publish(f"{MQTT_TOPIC}/DC/Battery_voltage_target_V", str(battery_voltage_target))
            client.publish(f"{MQTT_TOPIC}/XT/XT1_Battery_Current_A", str(xt1_batt_current))
            client.publish(f"{MQTT_TOPIC}/XT/XT2_Battery_Current_A", str(xt2_batt_current))
            client.publish(f"{MQTT_TOPIC}/XT/XT3_Battery_Current_A", str(xt3_batt_current))
            client.publish(f"{MQTT_TOPIC}/XT/XT4_Battery_Current_A", str(xt4_batt_current))


