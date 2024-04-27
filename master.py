import paho.mqtt.client as mqtt
import time
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
    int b=0;
    cout << a + b << endl;
    return 0;
}
"""
cpp_code_two = """
#include <iostream>
using namespace std;
int main() {
    int a=120912;
    int b=4000;
    cout << a + b << endl;
    return 0;
}
"""

Topic_Queue = []
Topic_Queue.append(TOPIC_1)
Topic_Queue.append(TOPIC_2)
print("---------------------------------------------------")


code_queue = []
code_queue.append(cpp_code)
code_queue.append(cpp_code_two)

print("Code Queue Data")

item = 0
for i in code_queue:
    item = item + 1
    print(f"Snippet {item} ")
    print(f"{i}")

print("---------------------------------------------------")


print("Topic Queue data")

for i in Topic_Queue:
    print(i)

print("---------------------------------------------------")

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code "+str(rc))
    publisher.subscribe(BACK_CHANNEL)
    print(f"Subscribed to {BACK_CHANNEL}")
    print("---------------------------------------------------")

def on_message(client, userdata, msg):
    print("---------------------------------------------------")
    json_data = json.loads(msg.payload.decode())
    # add topic back to the Topic_Queue
    responded_channel = json_data["topic"]
    Topic_Queue.append(responded_channel)
    print(f"Received acknowledgment from Child Node {responded_channel}")
    print(code_queue)
    print(json_data["output"])
    print("---------------------------------------------------")
    print("Current Status of Topic Queue on receiving the message = ", Topic_Queue)


publisher = mqtt.Client("Master_Node")
publisher.on_connect = on_connect
publisher.on_message = on_message
publisher.connect(MQTT_BROKER, MQTT_PORT, 60)
publisher.loop_start()
i = 11

while True:
    while len(code_queue) > 0:
        time.sleep(1)
        cpp_code = code_queue.pop()
        if len(Topic_Queue) > 0:
            # print(Topic_Queue)
            channel = Topic_Queue.pop()
            # print(Topic_Queue)
            json_payload = {
                "cpp_code": cpp_code,
                "topic": channel
            }
            json_str = json.dumps(json_payload)
            publisher.publish(channel, json_str)

        else:
            continue
    time.sleep(15)
    if i > 0:
        i = i - 1
        print(Topic_Queue)
