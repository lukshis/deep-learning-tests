def CollectLocations2(data):
    x = []
    y = []
    z = []
    locations = []
    for i in range(24):
        x.append(data[2+i*6])
        y.append(data[2+(i*6)+1])
        z.append(data[2+(i*6)+2])
    locations = [x, y, z]
    return locations

def CollectLocations2(data):
    locations = []
    for i in range(24):
        location = (data[2+i*6], data[2+(i*6)+1], data[2+(i*6)+2])
        locations.append(location)
    return locations