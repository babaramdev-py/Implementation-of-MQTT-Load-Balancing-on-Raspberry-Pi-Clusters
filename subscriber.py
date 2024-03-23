import paho.mqtt.client as mqtt
import subprocess

# Define constants
MQTT_BROKER = "localhost"  # broker address
MQTT_PORT = 1883  # mqtt port
TOPIC = "test/code"
BACK_CHANNEL = "test/output"

# Callback function when the subscriber receives a message
def on_message(client, userdata, msg):
    print("Received code from publisher:")
    print(msg.payload.decode())

    code = msg.payload.decode()
    output = execute_cpp_code(code)

    client.publish(BACK_CHANNEL, output)

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

    return result.stdout

subscriber = mqtt.Client("Subscriber")

# callback functions
subscriber.on_message = on_message
subscriber.on_connect = on_connect

subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)

subscriber.loop_start()

while True:
    pass
