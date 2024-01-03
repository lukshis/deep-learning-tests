""" def CollectLocations2(data):
    x = []
    y = []
    z = []
    locations = []
    for i in range(24):
        x.append(data[2+i*6])
        y.append(data[2+(i*6)+1])
        z.append(data[2+(i*6)+2])
    locations = [x, y, z]
    return locations """
import bpy

def CollectLocations2(data):
    locations = []
    for i in range(24):
        location = (data[2+i*6], data[2+(i*6)+1], data[2+(i*6)+2])
        locations.append(location)
    return locations

def CollectionExists(name):
    for collection in bpy.data.collections:
        if collection.name == name:
            return True
    return False

def ObjectExists(name):
    for object in bpy.data.objects:
        if object.name == name:
            return True
    return False

def HandLabel(data):
    if data[1] == 1:
        return "left"
    return "right"

def PoseLabel(data):
    match data[0]:
        case 0:
            return "thumbs_up"
        case 1:
            return "thumbs_down"
        case 2:
            return "ok"
        case 3:
            return "victory"
        case 4:
            return "horns"
        case 5:
            return "phone"
        case 6:
            return "one"
        case 7:
            return "point"
    return None