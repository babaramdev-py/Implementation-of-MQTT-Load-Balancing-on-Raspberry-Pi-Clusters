import time

import paho.mqtt.client as mqtt
import subprocess
import json 

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
INPUT_CHANNEL = "inputcode/node2"
BACK_CHANNEL = "outputcode/master"

def on_message(client, userdata, msg):
    time.sleep(0.5)
    print("Received code from publisher:")
    # print(msg.payload.decode())

    # Decode JSON payload
    try:
        json_data = json.loads(msg.payload.decode())
        code = json_data.get("cpp_code")
        topic = json_data.get("topic")
        print("Code Received from master")
        print(f"{code}")
        
        # Execute the received C++ code
        output = execute_cpp_code(code)

        # Create JSON payload for output
        output_payload = {
            "output": output,
            "topic": topic
        }
        # time.sleep(3)
        # Publish output payload back to master
        client.publish(BACK_CHANNEL, json.dumps(output_payload))
    except json.JSONDecodeError:
        print("Error decoding JSON payload")
    except Exception as e:
        print(f"Error processing message: {str(e)}")


def on_connect(client, userdata, flags, rc):
    subscriber.subscribe(INPUT_CHANNEL)
    print(f"Subscribed to {INPUT_CHANNEL}")
    print(f"Connected with code {rc}")

def execute_cpp_code(code):
    with open("temp2.cpp", "w") as file:
        file.write(code)

    try:
        subprocess.run(["g++", "temp2.cpp", "-o", "temp2.out"], check=True)
        result = subprocess.run(["./temp2.out"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

subscriber = mqtt.Client("Child_Node_Two")
subscriber.on_message = on_message
subscriber.on_connect = on_connect
subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)
subscriber.loop_start()

while True:
    pass
