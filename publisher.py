import paho.mqtt.client as mqtt
import time

# Define constants
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address
MQTT_PORT = 1883  # Default MQTT port
TOPIC = "test/code"
BACK_CHANNEL = "test/output"

# C++ code to print "Hello, world!"
cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
"""

# Callback function when the publisher connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code "+str(rc))
    # Publish the C++ code to the subscriber
    client.publish(TOPIC, cpp_code)

# Callback function when the publisher receives acknowledgment
def on_message(client, userdata, msg):
    print("Received acknowledgment from subscriber:")
    print(msg.payload.decode())

# Create MQTT client instance
publisher = mqtt.Client("Publisher")

# Set up callback functions
publisher.on_connect = on_connect
publisher.on_message = on_message

# Connect to MQTT broker
publisher.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the acknowledgment topic
publisher.subscribe(BACK_CHANNEL)

# Start the MQTT client loop
publisher.loop_start()

# Wait for acknowledgment
time.sleep(5)

# Disconnect from MQTT broker
publisher.disconnect()
