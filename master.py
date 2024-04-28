import paho.mqtt.client as mqtt
import time
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_1 = "inputcode/node1"
TOPIC_2 = "inputcode/node2"
TOPIC_3 = "inputcode/node3"
BACK_CHANNEL = "outputcode/master"


code_one = """
#include <iostream>
using namespace std;
int main() {
    int a=400;
    int b=200;
    cout << a + b << endl;
    return 0;
}
"""

code_two = """
#include <iostream>
using namespace std;
int main() {
    int a=120912;
    int b=4000;
    cout << a + b << endl;
    return 0;
}
"""

code_three = """
#include <iostream>
using namespace std;

int main() {
  cout << "Hello World!";
  return 0;
}
"""

code_four = """
#include <iostream>
using namespace std;
int main()
{
    int fact = 1;
	int rows = 4;
	for(int i = 1; i <= rows; i++)
    {
        fact = fact*i;
    }
    cout << "Factorial = " << fact << endl;
    return 0; 
}
"""

code_five = """
#include <iostream>
using namespace std;
int main()
{
    int fact = 1;
	int rows = 5;
	for(int i = 1; i <= rows; i++)
    {
        fact = fact*i;
    }
    cout << "Factorial = " << fact << endl;
    return 0; 
}


"""

code_six = """
#include <iostream>
using namespace std;
int main()
{
    int fact = 1;
	int rows = 6;
	for(int i = 1; i <= rows; i++)
    {
        fact = fact*i;
    }
    cout << "Factorial = " << fact << endl;
    return 0; 
}

"""

code_seven = """
#include <iostream>
using namespace std;
int main()
{
    int fact = 1;
	int rows = 7;
	for(int i = 1; i <= rows; i++)
    {
        fact = fact*i;
    }
    cout << "Factorial = " << fact << endl;
    return 0; 
}

"""

code_eight = """
#include <iostream>
using namespace std;

int main() {
    int number = 12345;
    int sum = 0;
    int temp = number;
    while(temp != 0) {
        sum += temp % 10;
        temp /= 10;
    }
    cout << "Sum of Digits of " << number << " is: " << sum << endl;
    return 0;
}

"""

code_nine = """
#include <iostream>
using namespace std;

int main() {
    float principal = 1000;
    float rate = 5.0;
    float time = 2.5;
    float interest = (principal * rate * time) / 100;
    cout << "Simple Interest: " << interest << endl;
    return 0;
}
"""

code_ten = """
#include <iostream>
using namespace std;

int main() {
    cout << "ASCII values of A-Z: ";
    for(char c = 'A'; c <= 'Z'; ++c) {
        cout << int(c) << " ";
    }
    cout << endl;
    return 0;
}

"""









Topic_Queue = []
Topic_Queue.append(TOPIC_1)
Topic_Queue.append(TOPIC_2)
Topic_Queue.append(TOPIC_3)
print("---------------------------------------------------")


code_queue = []
code_queue.append(code_one)
code_queue.append(code_two)
code_queue.append(code_three)
code_queue.append(code_four)
code_queue.append(code_five)
code_queue.append(code_six)
code_queue.append(code_seven)
code_queue.append(code_eight)
code_queue.append(code_nine)
code_queue.append(code_ten)

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
    print("---------------------------------------------------\n\n")
    json_data = json.loads(msg.payload.decode())
    # add topic back to the Topic_Queue
    responded_channel = json_data["topic"]
    Topic_Queue.append(responded_channel)
    print(f"Received acknowledgment from Child Node {responded_channel}")
    # print(code_queue)
    print(json_data["output"])
    print("---------------------------------------------------\n\n")


publisher = mqtt.Client("Master_Node")
publisher.on_connect = on_connect
publisher.on_message = on_message
publisher.connect(MQTT_BROKER, MQTT_PORT, 120)
publisher.loop_start()

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
    if len(code_queue) == 0:
        time.sleep(10)
        print(Topic_Queue)
