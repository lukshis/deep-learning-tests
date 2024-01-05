import json
import os
import numpy as np
import random

def ClassToNumber(class_string):
    match class_string:
        case "thumbs_up":
            return 0
        case "thumbs_down":
            return 1
        case "ok":
            return 2
        case "victory":
            return 3
        case "horns":
            return 4
        case "phone":
            return 5
        case "one":
            return 6
        case "point":
            return 7
    return None

def HandToNumber(hand):
    if hand == "left":
        return 1
    return 0

def ReadData(path="./data/", edit='none', loc=False, w_space=False):
    all_data = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            data = json.load(f)
            hand = 0
            label = ClassToNumber(data['class'])
            hand = HandToNumber(data['hand'])
            bones_rot = []
            #if loc:
            #    bones_loc = []
            w_loc = data['pose'][0]['world']['loc']
            for bone_data in data['pose']:
                if loc:
                    #print(w_loc)
                    if w_space:
                        location = [(bone_data['world']['loc']['x'] - w_loc['x']), (bone_data['world']['loc']['y'] - w_loc['y']), (bone_data['world']['loc']['z'] - w_loc['z'])]
                        if hand == 1:
                            location[1] = location[1] * -1
                    else:
                        location = [bone_data['comp']['loc']['x'], bone_data['comp']['loc']['y'], bone_data['comp']['loc']['z']]
                        if hand == 1:
                            location[0] = location[0] * -1
                            location[1] = location[1] * -1
                            location[2] = location[2] * -1
                    bones_rot.append(location)
                rotation = [bone_data['comp']['rot']['roll'], bone_data['comp']['rot']['pitch'], bone_data['comp']['rot']['yaw']]
                match edit:
                    case 'none':
                        None
                    case 'nor':
                        bone = [(item / 360) + 0.5 for item in bone]
                    case 'stan':
                        bone = [(item / 180) for item in bone]
                bones_rot.append(rotation)
            array = np.array(bones_rot)
            array = np.insert(array, 0, hand)
            array = np.insert(array, 0, label)
            array = array.flatten()
            all_data.append(array)
    return  np.array(all_data)

def GetData(path="./data/", augment=False, loc=False, w_space=False):
    all_data = ReadData(path, loc=loc, w_space=w_space)
      
    if augment:
        all_data = AugmentData(all_data)
    
    labels = all_data[:, :1]
    if loc:
        data = all_data[:, 14:]
    else:
        data = all_data[:, 8:]
    
    return labels, data

def AugmentData(data):
    augmented_data = np.array(data)
    for i in range(augmented_data.shape[0]):
        for j in range(7, 72):
            random.seed(i * j)
            random_v = random.random()
            augmented_data[i][j] = augmented_data[i][j] + (-1.0 + (random_v * (1.0 + 1.0)))
    full_data = np.concatenate((data, augmented_data), axis=0)
    return full_data

def ReadLocation(path):
    location_data = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            data = json.load(f)
            hand = 0
            label = ClassToNumber(data['class'])
            hand = HandToNumber(data['hand'])
            bone_loc = []
            for bone_data in data['pose']:
                location = [bone_data['comp']['loc']['x'], bone_data['comp']['loc']['y'], bone_data['comp']['loc']['z']]
                bone_loc.append(location)
            array = np.array(bone_loc)
            array = np.insert(array, 0, hand)
            array = np.insert(array, 0, label)
            array = array.flatten()
            location_data.append(array)
    return np.array(location_data)