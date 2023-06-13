import tensorflow
import keras
import numpy as np
import json
from PIL import Image #Python Environment lange instaliuoti ne PIL o Pillow, cia tas pats
import io
import socket
import time

CNN_model = tensorflow.keras.models.load_model("./results/Best_model.h5")

class_mapping = ['thumbs_up','thumbs_down','ok','victory']

def make_a_prediction(input):

    input_data = json.loads(input)

    pose = []

    for pose_data in input_data['rotations']:
        bone = [pose_data['roll'], pose_data['pitch'], pose_data['yaw']]
        pose.append(bone)

    pose = np.array(pose)
    pose = pose.flatten()
    pose = pose.reshape(1, 72, 1)

    # newsize = (28, 28)
    # gray_img = gray_img.resize(newsize)

    # img_array = []
    # img_array = np.asarray(gray_img)
    # img_array = img_array / 255.0
    # img_array = img_array.reshape(1,28,28,1)

    prediction = CNN_model.predict(pose,verbose=0)

    #prediction_list = numpy.argmax(CNN_model.predict(img_array,verbose=0), axis=1)
    prediction_list = np.argmax(prediction, axis=1)
    predicted_class = class_mapping[prediction_list[0]]
    print("Predicted class is " + predicted_class)

    #prediction_array = CNN_model.predict(img_array,verbose=0)
    #probability_percentage = prediction_array[0,prediction_list[0]]
    probability_percentage = prediction[0,prediction_list[0]]
    probability_percentage = round(probability_percentage*100, 2).astype('str')
    print("Probability percentage is " + probability_percentage + "%")

    return predicted_class, probability_percentage
    # return

IP = "127.0.0.1"
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
        buf = connection.recv(64*64)
        if len(buf) == 0:
            break
        #print(len(buf))
        c, p = make_a_prediction(buf)
        # timestamp = time.time_ns()
        # with open(f"{timestamp}.png", "wb") as binary_file:
        #     binary_file.write(buf)
        # with open(f"{timestamp}.txt", "w", encoding="utf-8") as result:
        #     result.write(f"{c};{p}")
        connection.sendall(f"{c};{p}".encode())
        
    connection.close()

# string_input = '{"rotations":[{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000},{"roll":-0.000000,"pitch":0.000000,"yaw":0.000000}]}'

# make_a_prediction(string_input)