import paho.mqtt.client as mqtt
import time
import queue
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_1 = "inputcode/node1"
TOPIC_2 = "inputcode/node2"
BACK_CHANNEL = "outputcode/master"

cpp_code = """
#include <iostream>
using namespace std;
int main() {
    int a=0;
    int b=1;
    cout << "Response From Child Node One" << endl;
    cout << a + b << endl;
    return 0;
}
"""
cpp_code_two = """
#include <iostream>
using namespace std;
int main() {
    int a=0;
    int b=2;
    cout << "Response From Child Node Two" << endl;
    cout << a + b << endl;
    return 0;
}
"""

code_queue = queue.Queue()
code_queue.put(cpp_code)
code_queue.put(cpp_code_two)

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code "+str(rc))
    publisher.subscribe(BACK_CHANNEL)
    print(f"Subscribed to {BACK_CHANNEL}")

def on_message(client, userdata, msg):
    time.sleep(1)
    print(f"Received acknowledgment from Child Node")
    json_data = json.loads(msg.payload.decode())
    print(json_data)

publisher = mqtt.Client("Master_Node")
publisher.on_connect = on_connect
publisher.on_message = on_message
publisher.connect(MQTT_BROKER, MQTT_PORT, 60)
publisher.loop_start()

while True:
    # Check if code queue is not empty
    # if not code_queue.empty():
        # Get code snippet from the queue
        # code = code_queue.get()

        # Prepare JSON payload
        time.sleep(1)
        json_payload = {
            "cpp_code": cpp_code,
            "topic": TOPIC_1  # Change this to dynamically assign topic based on queue
        }

        # Convert JSON payload to string
        json_str = json.dumps(json_payload)

        # Publish JSON payload to topic
        publisher.publish(TOPIC_1, json_str)
        print(f"Code published for {TOPIC_1}. Waiting for output...\n")

        # Sleep for a short interval before publishing to the next topic
        time.sleep(3)
        
        # Prepare JSON payload for the second topic
        json_payload["cpp_code"] = cpp_code_two
        json_payload["topic"] = TOPIC_2
        
        # Convert JSON payload to string
        json_str = json.dumps(json_payload)

        # Publish JSON payload to the second topic
        publisher.publish(TOPIC_2, json_str)
        print(f"Code published for {TOPIC_2}. Waiting for output...\n")

        # Sleep for a short interval before continuing to the next iteration
        time.sleep(3)
