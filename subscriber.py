import paho.mqtt.client as mqtt
import subprocess

# Define constants
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address
MQTT_PORT = 1883  # Default MQTT port
TOPIC = "test/code"
BACK_CHANNEL = "test/output"

# Callback function when the subscriber receives a message
def on_message(client, userdata, msg):
    print("Received code from publisher:")
    print(msg.payload.decode())

    # Execute the received C++ code
    code = msg.payload.decode()
    output = execute_cpp_code(code)

    # Publish the output back to the publisher
    client.publish(BACK_CHANNEL, output)

# Function to execute C++ code and return the output
def on_connect(client, userdata, flags, rc):
    subscriber.subscribe(TOPIC)
    print(f"Subscribed to {TOPIC}")
    print(f"Connected with code {rc}")

def execute_cpp_code(code):
    # Write the C++ code to a file
    with open("temp.cpp", "w") as file:
        file.write(code)

    # Compile the C++ code
    subprocess.run(["g++", "temp.cpp", "-o", "temp.out"])

    # Execute the compiled binary and capture the output
    result = subprocess.run(["./temp.out"], capture_output=True, text=True)

    # Return the output
    return result.stdout

# Create MQTT client instance
subscriber = mqtt.Client("Subscriber")

# Set up callback functions
subscriber.on_message = on_message
subscriber.on_connect = on_connect
# Connect to MQTT broker
subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)

subscriber.loop_start()
# Subscribe to the code topic
# Start the MQTT client loop
while True:
    pass
