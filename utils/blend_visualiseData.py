import bpy
import bmesh
import os
from parseData import ReadData
from utilities import CollectLocations2

path = os.path.abspath("D:\python-workspaces\deep-learning-tests\data")
#path = "../data/"
all_data = ReadData(path, loc=True)
points = [[0, 1],
          [1, 2, 3, 4, 5, 19],
          [1, 6, 7, 8, 20],
          [1, 9, 10, 11, 21],
          [1, 12, 13, 14, 22],
          [1, 15, 16, 17, 18, 23]]

def CreateVerts(data, points):
    
    loc = CollectLocations2(data)

    mesh = bpy.data.meshes.new("mesh")
    obj = bpy.data.objects.new("Object", mesh)

    #bpy.data.scenes[0].collection.objects.link(obj)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for v in loc:
        v = [i * 0.1 for i in v]
        bm.verts.new(v)

    bm.verts.ensure_lookup_table()

    for p in points:
        for i in range(len(p)-1):
            bm.edges.new((bm.verts[p[i]], bm.verts[p[i+1]]))
    
    bm.to_mesh(mesh)
    bm.free()
    return

CreateVerts(all_data[0], points)