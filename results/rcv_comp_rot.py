import tensorflow
import numpy as np
import json
import socket

modelfile = "model_comp_rot.h5"
model = tensorflow.keras.models.load_model("./results/" + modelfile)

class_mapping = ['thumbs_up','thumbs_down','ok','victory', 'horns', 'phone', 'one', 'point']

def MakePrediction(input):
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
    for pose_data in input_data['pose']:
        bone = [pose_data['comp']['rot']['roll'], pose_data['comp']['rot']['pitch'], pose_data['comp']['rot']['yaw']]
        pose.append(bone)


    pose = np.array(pose)
    pose = pose[2:]
    pose = pose.flatten()
    pose = pose.reshape(1, 66, 1)

    prediction = model.predict(pose,verbose=0)

    prediction_list = np.argmax(prediction, axis=1)
    #predicted_class = class_mapping[prediction_list[0]]
    #probability_percentage = prediction[0,prediction_list[0]]
    #probability_percentage = round(probability_percentage*100, 2).astype('str')

    #print("Predicted class: " + predicted_class + " | Probability: " + probability_percentage + "%")
    #print("{0}, {1}".format(prediction_list[0], prediction[0,prediction_list[0]]))
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