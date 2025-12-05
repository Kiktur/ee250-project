import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO       # <<< ADDED
import time                   # <<< ADDED

"""This function (or "callback") will be executed when this client receives
a connection acknowledgement packet response from the server. """

rec_topic="vagutier_ee250_project_1"

# ========== SERVO SETUP (ADDED) ==========
SERVO1_PIN = 17   # <<< ADDED  (GPIO17)
SERVO2_PIN = 18   # <<< ADDED  (GPIO18)

GPIO.setmode(GPIO.BCM)              # <<< ADDED
GPIO.setup(SERVO1_PIN, GPIO.OUT)    # <<< ADDED
GPIO.setup(SERVO2_PIN, GPIO.OUT)    # <<< ADDED

pwm1 = GPIO.PWM(SERVO1_PIN, 50)     # <<< ADDED  (50 Hz)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)     # <<< ADDED

pwm1.start(0)                       # <<< ADDED
pwm2.start(0)                       # <<< ADDED

def set_angle(pwm, angle):          # <<< ADDED
    duty = 2.5 + (angle / 18.0)     # <<< ADDED
    pwm.ChangeDutyCycle(duty)       # <<< ADDED
    time.sleep(0.4)                 # <<< ADDED

def move_servos_sequence():         # <<< ADDED
    # center both                   # <<< ADDED
    set_angle(pwm1, 90)             # <<< ADDED
    set_angle(pwm2, 90)             # <<< ADDED
    time.sleep(1)                   # <<< ADDED

    # move servo 1                  # <<< ADDED
    set_angle(pwm1, 0)              # <<< ADDED
    time.sleep(2)                   # <<< ADDED  (2 second delay)

    # move servo 2                  # <<< ADDED
    set_angle(pwm2, 0)              # <<< ADDED
    time.sleep(1)                   # <<< ADDED
# =========================================


def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that,
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""

    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe(rec_topic)
   
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add(rec_topic, on_action_message)


"""This object (functions are objects!) serves as the default callback for
messages received when another node publishes a message this client is
subscribed to. By "default,"" we mean that this callback is called if a custom
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    # print("Custom callback  - topic: "+msg.payload.decode())
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))


#Custom message callback.
def on_action_message(client, userdata, message):
   # <<< CHANGED: this is where your behavior goes
   print("Custom callback  - action: "+message.payload.decode())
   print("Action was sent")
   # run your servo sequence whenever any message arrives:
   move_servos_sequence()          # <<< ADDED



if __name__ == '__main__':
   
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    """Connect using the following hostname, port, and keepalive interval (in
    seconds). We added "host=", "port=", and "keepalive=" for illustrative
    purposes. You can omit this in python.
       
    The keepalive interval indicates when to send keepalive packets to the
    server in the event no messages have been published from or sent to this
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""    
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)


    client.loop_forever()