import paho.mqtt.client as mqtt
import tkinter as tk


rec_topic="vagutier_ee250_project"
send_topic="vagutier_ee250_project_1"

# emotion_label = None

def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that, 
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""

    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe(rec_topic)
    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add(rec_topic, on_emotion_message)


def on_message(client, userdata, msg):
    # print("Custom callback  - topic: "+msg.payload.decode())
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))


neutral_counter = 0
happy_counter = 0
sad_counter = 0
angry_counter = 0
fear_counter = 0
surprise_counter = 0
disgust_counter = 0
total_counter = 0

#Custom message callback.
def on_emotion_message(client, userdata, message):
    # print("Custom callback  - emotion: "+message.payload.decode())
    emotion = message.payload.decode()
    global total_counter, neutral_counter, happy_counter, sad_counter, angry_counter, fear_counter, surprise_counter, disgust_counter
    emotion_text = f"Current emotion is: {emotion}"
    total_counter += 1
    match emotion:
        case "Neutral":
            neutral_counter += 1
        case "Happy":
            happy_counter += 1
        case "Sad":
            sad_counter += 1
        case "Angry":
            angry_counter += 1
        case "Fear":
            fear_counter += 1
        case "Surprise":
            surprise_counter += 1
        case "Disgust":
            disgust_counter += 1
        case _:
            print("Unknown emotion")

    neutral_text = f"Neutral: {round(100 * (neutral_counter / total_counter), 2)}%"   
    happy_text = f"Happy: {round(100 * (happy_counter / total_counter), 2)}%" 
    sad_text = f"Sad: {round(100 * (sad_counter / total_counter), 2)}%" 
    angry_text = f"Angry: {round(100 * (angry_counter / total_counter), 2)}%" 
    fear_text = f"Fear: {round(100 * (fear_counter / total_counter), 2)}%" 
    surprise_text = f"Surprise: {round(100 * (surprise_counter / total_counter), 2)}%" 
    disgust_text = f"Disgust: {round(100 * (disgust_counter / total_counter), 2)}%" 

    window.after(0, update_emotion_labels, emotion_text, neutral_text, happy_text, sad_text, angry_text, fear_text, surprise_text, disgust_text)


def button_click():
    client.publish(send_topic, "Action")
    print("Button was clicked")

def update_emotion_labels(emotion_text, neutral_text, happy_text, sad_text, angry_text, fear_text, surprise_text, disgust_text):
    emotion_label.config(text=emotion_text)
    neutral_label.config(text=neutral_text)
    happy_label.config(text=happy_text)
    sad_label.config(text=sad_text)
    angry_label.config(text=angry_text)
    fear_label.config(text=fear_text)
    surprise_label.config(text=surprise_text)
    disgust_label.config(text=disgust_text)


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


    window = tk.Tk()
    window.title("EE250 Project")
    window.geometry("600x400")

    emotion_label = tk.Label(window, text="Waiting for message...", font=("Arial", 16))
    emotion_label.pack(pady=20)

    description_label = tk.Label(window, text="Distribution of emotions over session:", font=("Arial", 14))
    description_label.pack(pady=20)

    neutral_label = tk.Label(window, text="Neutral: 0%", font=("Arial", 12))
    neutral_label.pack()

    happy_label = tk.Label(window, text="Happy: 0%", font=("Arial", 12))
    happy_label.pack()

    sad_label = tk.Label(window, text="Sad: 0%", font=("Arial", 12))
    sad_label.pack()

    angry_label = tk.Label(window, text="Angry: 0%", font=("Arial", 12))
    angry_label.pack()

    fear_label = tk.Label(window, text="Fear: 0%", font=("Arial", 12))
    fear_label.pack()

    surprise_label = tk.Label(window, text="Surprise: 0%", font=("Arial", 12))
    surprise_label.pack()

    disgust_label = tk.Label(window, text="Disgust: 0%", font=("Arial", 12))
    disgust_label.pack()



    button = tk.Button(window, text="Send Action", command=button_click)
    button.pack()
    client.loop_start()
    window.mainloop()

    client.loop_stop()
    client.disconnect()

    