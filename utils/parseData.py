import json
import os
import numpy as np

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
    return None

def HandToNumber(hand):
    if hand == "left":
        return 1
    return 0

def ReadData(path, edit='none',loc=False):
    all_data = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            data = json.load(f)
            hand = 0
            label = ClassToNumber(data['class'])
            hand = HandToNumber(data['hand'])
            bones_rot = []
            if loc:
                bones_loc = []
            for bone_data in data['pose']:
                rotation = [bone_data['comp']['rot']['roll'], bone_data['comp']['rot']['pitch'], bone_data['comp']['rot']['yaw']]
                match edit:
                    case 'none':
                        None
                    case 'nor':
                        bone = [(item / 360) + 0.5 for item in bone]
                    case 'stan':
                        bone = [(item / 180) for item in bone]
                bones_rot.append(rotation)
                if loc:
                    location = [bone_data['comp']['loc']['x'], bone_data['comp']['loc']['y'], bone_data['comp']['loc']['z']]
                    bones_loc.append(location)
            array = np.array(bones_rot)
            array = np.insert(array, 0, hand)
            array = np.insert(array, 0, label)
            array = array.flatten()
            all_data.append(array)
    return  np.array(all_data)

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