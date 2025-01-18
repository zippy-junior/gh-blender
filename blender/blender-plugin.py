# This example assumes we have a mesh object selected

import bpy
import bmesh
import requests

def get_mesh():
    r = requests.get("http://localhost:8000/obj")
    return r.json()

mesh = get_mesh()

#v, f = data.split("\n\n")
#split_data = data.split("\n")

vertices = [
   tuple([float(coord) for coord in v_data.split(" ")[1:]]) for v_data in mesh.get("v").split("\n")
]

faces = [
   tuple([int(coord) for coord in f_data.split(" ")[1:]]) for f_data in mesh.get("f").split("\n")
]

## Create a new mesh
mesh = bpy.data.meshes.new(name="NewMesh")

## Add vertices and faces to the mesh
mesh.from_pydata(vertices, [], faces)

## Create a new object using the mesh
obj = bpy.data.objects.new(name="NewObject", object_data=mesh)

## Link the object to the current scene
bpy.context.collection.objects.link(obj)

## Update the mesh
mesh.update()