
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import os

app = Flask(__name__)
#app = Flask(__name__, template_folder='/var/www/html/templates')

#background process happening without any refreshing
@app.route('/left')
def left():
    print ("Left")
    os.system("python servo.py 1 2 0.1 1")       
    return ("nothing")

@app.route('/center')
def center():
    print ("Center")
    os.system("python servo.py 89 90 0.3 1")       
    return ("nothing")

@app.route('/right')
def right():
    print ("Right")
    os.system("python servo.py 179 180 0.1 1")       
    return ("nothing")


@app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        
        return render_template('index.html', res_str=result)
                        
    return render_template('index.html')

#global every_person = []
temp_person = ""
def gen(camera):
    while True:
        frame = camera.get_frame()
        
        currentPerson = camera.get_person()
        if currentPerson != temp_person:
            #every_person.append(currentPerson)
            print(currentPerson)
            temp_person = currentPerson
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

connflag = False

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
    while 1==1:
        sleep(5)
        if connflag == True:
            paylodmsg0="{"
            paylodmsg1 = "\"Name\": \""
            paylodmsg2="\"}"
            person = temp_person
            paylodmsg = "{} {} {}".format(paylodmsg0, paylodmsg1, person, paylodmsg2)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)     #converting to json format
            mqttc.publish("SquidGameTest", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg sent: uploading names" ) # Print sent temperature msg on console
            print(paylodmsg_json)

        else:
            print("waiting for connection...")
