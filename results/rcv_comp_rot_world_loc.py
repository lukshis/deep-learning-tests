import tensorflow
import numpy as np
import json
import socket
import time

modelfile = "model_comp_rot_world_loc.h5"
model = tensorflow.keras.models.load_model("./results/" + modelfile)

class_mapping = ['thumbs_up','thumbs_down','ok','victory', 'horns', 'phone', 'one', 'point']

def MakePrediction(input):
    start_time = time.time()

    if not input.startswith(b"{\"class\":"):
        print("bad start")
        return 0, 0.0
    if not input.endswith(b"}]}"):
        print("bad end")
        return 0, 0.0
    if b"}{" in input:
        print("two at a time")
        return 0, 0.0
    input_data = json.loads(input)
    pose = []
    w_loc = input_data['pose'][0]['world']['loc']
    for pose_data in input_data['pose']:
        bone = [(pose_data['world']['loc']['x'] - w_loc['x']), (pose_data['world']['loc']['y']  - w_loc['y']), (pose_data['world']['loc']['z'] - w_loc['z'])]
        pose.append(bone)
        bone = [pose_data['comp']['rot']['roll'], pose_data['comp']['rot']['pitch'], pose_data['comp']['rot']['yaw']]
        pose.append(bone)

    pose = np.array(pose)
    pose = pose[4:]
    pose = pose.flatten()
    pose = pose.reshape(1, 132, 1)
    duration = time.time() - start_time

    prediction_time = time.time()
    prediction = model.predict(pose,verbose=0)
    prediction_duration = time.time() - prediction_time
    prediction_list = np.argmax(prediction, axis=1)
    #predicted_class = class_mapping[prediction_list[0]]
    #probability_percentage = prediction[0,prediction_list[0]]
    #probability_percentage = round(probability_percentage*100, 2).astype('str')

    #print("Predicted class: " + predicted_class + " | Probability: " + probability_percentage + "%")
    #print("{0}, {1}".format(prediction_list[0], prediction[0,prediction_list[0]]))
    print("Prediction time: {} Function time: {}".format(prediction_duration, duration))
    return prediction_list[0], prediction[0,prediction_list[0]]
    #return predicted_class, probability_percentage

IP = "0.0.0.0"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(5)

print("---Starting the predictor---")

while True:
    print("Waiting for connection...")
    connection, addr = sock.accept()
    print("Accepted connection.")

    while True:
        pose_data = connection.recv(8*1024)
        if len(pose_data) == 0:
            break
        c, p = MakePrediction(pose_data)
        #print("" + c + " " + str(p))
        connection.sendall(f"{c};{p}".encode())

    connection.close()
    print("---Connection closed---")