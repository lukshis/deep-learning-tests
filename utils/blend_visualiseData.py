import bpy
import bmesh
import os
from parseData import ReadData
import blend_utilities as bu

path = os.path.abspath("D:\Repositories\python-workspaces\deep-learning-tests\data")
#path = "../data/"
all_data = ReadData(path, loc=True)
points = [[0, 1],
          [1, 2, 3, 4, 5, 19],
          [1, 6, 7, 8, 20],
          [1, 9, 10, 11, 21],
          [1, 12, 13, 14, 22],
          [1, 15, 16, 17, 18, 23]]

def CreateVerts(data, points):
    c = 0
    for data in all_data:
        loc = bu.CollectLocations2(data)
        #creates a new collection for a hand pose class (if it does not exist)
        poseLabel = bu.PoseLabel(data)
        if not bu.CollectionExists(poseLabel):
            new_collection = bpy.data.collections.new(poseLabel)
            bpy.context.scene.collection.children.link(new_collection)
        collection = bpy.context.scene.collection.children[poseLabel]
        #creats a new mesh object for a hand pose (if it does not exist)
        hand = bu.HandLabel(data)
        if not bu.ObjectExists("{}-{}-hand".format(c, hand)):    
            mesh = bpy.data.meshes.new("mesh{}".format(c))
            obj = bpy.data.objects.new("{}-{}-hand".format(c, hand), mesh)
            collection.objects.link(obj)
        obj = bpy.data.objects["{}-{}-hand".format(c, hand)]
        
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
        c = c + 1
    return

CreateVerts(all_data, points)