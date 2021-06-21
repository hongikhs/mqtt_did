from tkinter import *
import paho.mqtt.client as mqtt
import csv

f = open('mqtt_sub.csv', 'r', encoding='utf-8')
g = csv.reader(f)
server, port = next(g)
name, topic = next(g)
f.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

msg_index = 0
def on_message(client, userdata, msg):
    global msg_index
    print(msg.topic+" "+str(msg.payload, 'utf-8'))
    lb_msg.insert(msg_index, str(msg.payload, 'utf-8'))
    #msg_index += 1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, int(port), 60)
client.loop_start()

def publish():
    name = t_name.get(1.0, END+"-1c")
    topic = t_topic.get(1.0, END+"-1c")
    msg = t_msg.get(1.0, END+"-1c")
    print(msg)
    client.publish(topic, '[' + name + '] ' + msg)

    try:
        f = open('mqtt_pub.csv', 'w', encoding='utf-8', newline='')
        g = csv.writer(f)
        g.writerow([server, port])
        g.writerow([name, topic])
        f.close()
    except:
        name = ''
        topic = ''


root = Tk()
root.attributes('-fullscreen', True)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
df = ('Arial', 15)
bf = ('Arial', 60, 'bold')

root.title(name)
f_name = Frame(root)

l_name = Label(f_name, text='이름')
l_name.pack(side='left')
t_name = Text(f_name, height=1, width=10)
t_name.insert(1.1, name)
t_name.pack(side='left')

l_topic = Label(f_name, text='토픽')
l_topic.pack(side='left')
t_topic = Text(f_name, height=1, width=20)
t_topic.insert(1.1, topic)
t_topic.pack(side='left')

f_name.pack()

lb_msg = Listbox(root, font=bf, width=43)
lb_msg.pack()

b_pub = Button(root, text='지우기', width=10, command=publish)
b_pub.pack()

root.mainloop()