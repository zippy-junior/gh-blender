"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable
        b: The b output variable"""

__author__ = "alexey"

import Rhino.Geometry as rg
from urllib2 import (
    Request,
    urlopen,
    HTTPError,
    URLError
)
import json


def mesh_to_obj(mesh):
    """Convert a Rhino mesh to OBJ format."""
    vertex_lines = []

    # Add vertices
    for vertex in mesh.Vertices:
        vertex_lines.append("v "+str(vertex.X)+" "+str(vertex.Y)+" "+str(vertex.Z))

    face_lines = []
    # Add faces
    for face in mesh.Faces:
        if face.IsQuad:
            # Quad face (4 vertices)
            face_lines.append("f "+str(face.A)+" "+str(face.B)+" "+str(face.C)+" "+str(face.D))
        else:
            # Triangle face (3 vertices)
            face_lines.append("f "+str(face.A)+" "+str(face.B)+" "+str(face.C))

    # Join lines into a single string
    return {"v": vertex_lines, "f": face_lines}


def test_request(url):
    """
    Sends JSON data to a specified URL using an HTTP POST request.

    :param url: The URL to send the request to.
    :param data: A Python dictionary containing the data to be sent as JSON.
    :return: The response from the server.
    """
    # Convert the data dictionary to a JSON string

    # Set up the request headers

    # Create the request object
    req = Request(url)

    try:
        # Send the request and get the response
        response = urlopen(req)
        response_data = response.read()
        response_code = response.getcode()
        return {
            'status_code': response_code,
            'data': response_data,
        }
    except HTTPError as e:
        # Handle HTTP errors
        return {
            'status_code': e.code,
            'data': e.read(),
        }
    except URLError as e:
        # Handle URL errors (e.g., network issues)
        return {
            'status_code': None,
            'data': str(e.reason),
        }


def send_obj_data(url, obj_txt):
    """
    Sends JSON data to a specified URL using an HTTP POST request.

    :param url: The URL to send the request to.
    :param data: A Python dictionary containing the data to be sent as JSON.
    :return: The response from the server.
    """
    # Convert the data dictionary to a JSON string
    json_data = json.dumps(obj_txt)

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Create the request object
    req = Request(url, json_data, headers)

    try:
        # Send the request and get the response
        response = urlopen(req)
        response_data = response.read()
        response_code = response.getcode()
        return {
            'status_code': response_code,
            'data': response_data,
        }
    except HTTPError as e:
        # Handle HTTP errors
        return {
            'status_code': e.code,
            'data': e.read(),
        }
    except URLError as e:
        # Handle URL errors (e.g., network issues)
        return {
            'status_code': None,
            'data': str(e.reason),
        }


# Input: Mesh from Grasshopper
mesh = x  # noQa f821 # 'x' is the default input variable in Grasshopper Python

# Convert mesh to OBJ
if mesh and isinstance(mesh, rg.Mesh):
    a = mesh.Vertices
    obj_text = mesh_to_obj(mesh)
    a = obj_text.get("v")
    b = obj_text.get("f")
    res = send_obj_data("http://127.0.0.1:8000/obj", obj_text)
    c = [res["status_code"], res["data"]]
else:
    obj_text = "Invalid input. Please provide a valid mesh."
