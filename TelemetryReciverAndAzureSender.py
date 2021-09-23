# !/usr/bin/env python

from __future__ import print_function
import sys
import os
import time
from abc import abstractmethod

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm_sync import FeatureAudioADPCMSync
from azure.iot.device import IoTHubDeviceClient, Message

# Presentation message.
INTRO = """############################
SensorTile Data Sender
############################"""

# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iotc-a7f92cb1-1d08-42db-9eeb-65f61e621b04.azure-devices.net;DeviceId=1fveb3ctdp5;SharedAccessKey=HuPoka/yOUI1fHRzX4fgipZxcVo4EpmnbkeKYdGbi80="
# Bluetooth Scanning time in seconds (optional).
SCANNING_TIME_s = 5

# Layout message
MSG_TXT = '{{"temperature": {temperature},"pressure": {pressure},"acceleration_x": {acceleration_x},"acceleration_y": {acceleration_y}, "acceleration_z": {acceleration_z}, "gyroscope_x": {gyroscope_x}, "gyroscope_y": {gyroscope_y}, "gyroscope_z": {gyroscope_z}, "magneticflux_x": {magneticflux_x}, "magneticflux_y": {magneticflux_y}, "magneticflux_z": {magneticflux_z}}}'


# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
class MyManagerListener(ManagerListener):

    # This method is called whenever a discovery process starts or stops.
    def on_discovery_change(self, manager, enabled):
        #print('Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            print()

    # This method is called whenever a new node is discovered.
    def on_node_discovered(self, manager, node):
        print('New device discovered: %s.' % (node.get_name()))


# Implementation of the interface used by the Node class to notify that a node has updated its status.
class MyNodeListener(NodeListener):

    # To be called whenever a node connects to a host.
    def on_connect(self, node):
        print('Device %s connected.' % (node.get_name()))

    # To be called whenever a node disconnects from a host.
    def on_disconnect(self, node, unexpected=False):
        print('Device %s disconnected%s.' % \
              (node.get_name(), ' unexpectedly' if unexpected else ''))
        if unexpected:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)



# Printing intro.
def print_intro():
    print('\n' + INTRO + '\n')


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def iothub_client_telemetry(device):
    try:
        client = iothub_client_init()
        features = listfeatures(device)
        print("Sending periodic messages, press Ctrl-C to exit")

        while True:
            # Build the message with telemetry values.
            temperature = (readsensor(device, features[2])).split()
            pressure = (readsensor(device, features[3])).split()
            acceleration = (readsensor(device, features[6])).split()
            gyroscope = (readsensor(device, features[5])).split()
            magneticflux = (readsensor(device, features[4])).split()
            msg_txt_formatted = MSG_TXT.format(temperature=temperature[1], pressure=pressure[1], acceleration_x=acceleration[3], acceleration_y=acceleration[6], acceleration_z=acceleration[9], gyroscope_x=gyroscope[3], gyroscope_y=gyroscope[6], gyroscope_z=gyroscope[9], magneticflux_x=magneticflux[3], magneticflux_y=magneticflux[6], magneticflux_z=magneticflux[9])
            message = Message(msg_txt_formatted)

            # Send the message.
            client.send_message(message)
            print(message)

            # Interval between two messages
            time.sleep(10)
    except KeyboardInterrupt:
        print("IoTHubClient stopped")


def connect_ble(MAC):
    # Creating Bluetooth Manager.
    manager = Manager.instance()
    manager_listener = MyManagerListener()
    manager.add_listener(manager_listener)

    while True:
        # Synchronous discovery of Bluetooth devices.
        print('Scanning Bluetooth devices...\n')
        manager.discover(SCANNING_TIME_s)

        # Getting discovered devices.
        discovered_devices = manager.get_nodes()
        if not discovered_devices:
            print('No Bluetooth devices found. Exiting...\n')
            sys.exit(0)

        # Checking discovered devices.
        device = None
        for discovered in discovered_devices:
            if discovered.get_tag() == MAC:  # Compares discovered devices MAC with the MAC provided
                device = discovered  # If found, then that is the device
                break
        if not device:
            print('Device not found...\n')
            sys.exit(0)

        # Connecting to the devices.
        node_listener = MyNodeListener()
        device.add_listener(node_listener)
        print('Connecting to %s...' % (device.get_name()))
        if not device.connect():
            print('Connection failed.\n')
            sys.exit(0)
        print('Connection done. \n')
        print('Start logging \n')
        return device  # Returns the device object


def listfeatures(device):  # Returns all all the features of the device
    # Getting features.
    features = device.get_features()
    return features


def readsensor(device, sensor):  # Returns a single data of any sensor
    device.enable_notifications(sensor)
    dado = '0'
    if device.wait_for_notifications(3):
        dado = str(sensor)
    device.disable_notifications(sensor)
    return dado


def main(argv):
    # Printing intro.
    print_intro()

    try:
        SENSORTILE_MAC = 'db:09:49:c5:a2:0d'
        device = connect_ble(SENSORTILE_MAC)
        iothub_client_telemetry(device)

    except KeyboardInterrupt:
        try:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
