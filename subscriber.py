import paho.mqtt.client as mqtt
import subprocess

MQTT_BROKER = "localhost"  # broker address
MQTT_PORT = 1883  # mqtt port
TOPIC = "test/code"
BACK_CHANNEL = "test/output"

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
    with open("temp.cpp", "w") as file:
        file.write(code)

    subprocess.run(["g++", "temp.cpp", "-o", "temp.out"])

    result = subprocess.run(["./temp.out"], capture_output=True, text=True)

    return result.stdout

subscriber = mqtt.Client("Subscriber")

subscriber.on_message = on_message
subscriber.on_connect = on_connect

subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)

subscriber.loop_start()

while True:
    pass
