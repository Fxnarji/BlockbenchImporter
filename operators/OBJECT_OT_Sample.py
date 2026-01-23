import bpy  # type: ignore
from ..constants import get_operator
import json
from pathlib import Path
from mathutils import Vector

FACE_KEY = {
    0: "north",
    1: "south",
    2: "down",
    3: "east",
    4: "up",
    5: "west",
}



# Define the operator to snap FK bones to IK bones
class OBJECT_OT_Sample(bpy.types.Operator):
    bl_idname = get_operator("operator")
    bl_description = "Renames selected Object to Hello World"
    bl_label = "Renames selected object to Hello World"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        path = Path("/home/fxnarji/Github/BlockbenchImporter/test_data/Test3.blockymodel")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            parent = bpy.data.objects.new(str(path.name.split('.')[0]), None)
            bpy.context.collection.objects.link(parent)
            
            for root in data["nodes"]:
                walk_node(root, parent)

            parent.rotation_euler = (1.5708, 0, 0)

        return {'FINISHED'}


def walk_node(node, parent=None):
    name = node.get("name", "Node")

    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'CUBE'
    empty.rotation_mode = 'QUATERNION'

    bpy.context.collection.objects.link(empty)

    if parent:
        empty.parent = parent

    # --- position (local) ---
    pos = node.get("position")
    if pos:
        x = pos["x"]
        y = pos["y"]
        z = pos["z"]
    shape = node.get("shape")
    if shape and shape["offset"]:
        offset = shape["offset"]
        x += offset["x"]
        y += offset["y"]
        z += offset["z"]

    empty.location = (x,y,z)

    # --- rotation (local quaternion) ---
    quat = node.get("orientation")
    if quat:
        # Blender wants (w, x, y, z)
        empty.rotation_quaternion = (
            quat["w"],
            quat["x"],
            quat["y"],
            quat["z"],
        )

    # --- scale (local) ---
    shape = node.get("shape")
    if shape:
        stretch = shape.get("stretch")
        if stretch:
            empty.scale = (
                stretch["x"],
                stretch["y"],
                stretch["z"],
            )

    shape = node.get("shape")
    if shape:
    # --- shape (box) ---
        if shape["type"] == "box":


            box = create_box_v2(name,shape=shape)
            
            #generate_box_uv(box_mesh, width=64, height=32, shape=shape)

            box.parent = empty
    
    # --- shape (quad) ---
        if shape["type"] == "quad":
            size = shape["settings"]["size"]
            stretch = shape.get("stretch", {"x":1,"y":1,"z":1})

            quad = create_quad(
                name,
                (
                    size["x"] * stretch["x"],
                    size["y"] * stretch["y"],
                )
            )

            quad.parent = empty
    
    # recurse
    for child in node.get("children", []):
        walk_node(child, empty)

def create_box(name, shape):
    mesh = bpy.data.meshes.new(name)


    size = shape["settings"]["size"]

    sx = size["x"] 
    sy = size["y"]
    sz = size["z"]



    verts = [
        (-sx/2, -sy/2, -sz/2),
        ( sx/2, -sy/2, -sz/2),
        ( sx/2,  sy/2, -sz/2),
        (-sx/2,  sy/2, -sz/2),
        (-sx/2, -sy/2,  sz/2),
        ( sx/2, -sy/2,  sz/2),
        ( sx/2,  sy/2,  sz/2),
        (-sx/2,  sy/2,  sz/2),
    ]

    faces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Create UV layer
    uv_layer = mesh.uv_layers.new(name="UVMap")
    uvs = uv_layer.data


    texture_layout = shape["textureLayout"]
    tex_width = 32
    tex_height = 32
    for poly in mesh.polygons:
        face_name = name_face_by_normal(poly.normal)

        # Convert vertex coordinates to Vectors to get dimensions of face
        v0 = Vector(verts[poly.vertices[0]])
        v1 = Vector(verts[poly.vertices[1]])
        v3 = Vector(verts[poly.vertices[3]])

        face_width = (v1 - v0).length
        face_height = (v3 - v0).length



        # Default to full-meter UVs if no texture layout is provided
        if texture_layout and face_name in texture_layout:
            offset = texture_layout[face_name]["offset"]

            offset_x = offset["x"]
            offset_y = offset["y"]

            # Original math (top-left = 0,0)
            left   = offset_x / tex_width
            right  = (offset_x + face_width) / tex_width
            bottom = offset_y / tex_height
            top    = (offset_y + face_height) / tex_height

            # Convert to Blender UV space (bottom-left = 0,0)
            blender_bottom = 1.0 - top    # flip V
            blender_top    = 1.0 - bottom

            # Left/right stay the same
            blender_left   = left
            blender_right  = right

            # Final corners in Blender UV space
            corners = [
                (blender_left, blender_bottom),   # bottom-left
                (blender_right, blender_bottom),  # bottom-right
                (blender_right, blender_top),     # top-right
                (blender_left, blender_top),      # top-left
            ]


        else:
            left = 0
            right = face_width / tex_width
            bottom = 0
            top = face_height / tex_height



        for i in range(poly.loop_start, poly.loop_start + poly.loop_total):
            uvs[i].uv = corners[i - poly.loop_start]

        

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def create_quad(name, size):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)

    bpy.context.collection.objects.link(obj)

    sx, sy = size
    verts = [
        (-sx/2, -sy/2, 0),
        ( sx/2, -sy/2, 0),
        ( sx/2,  sy/2, 0),
        (-sx/2,  sy/2, 0),
    ]
    faces = [
        (0,1,2,3),
        (4,5,6,7),
    ]

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def rotate_corners(corners, angle):
    """Rotate corners clockwise by 0, 90, 180, or 270 degrees."""
    steps = (angle // 90) % 4
    return [corners[(i - steps) % 4] for i in range(4)]

def name_face_by_normal(normal):
    x, y, z = normal
    if abs(x) > abs(y) and abs(x) > abs(z):
        return "right" if x > 0 else "left"
    elif abs(y) > abs(x) and abs(y) > abs(z):
        return "top" if y > 0 else "bottom"
    else:  # Z is dominant
        return "back" if z > 0 else "front"


def create_box_v2(name, shape):
    mesh = bpy.data.meshes.new(name)

    size = shape["settings"]["size"]
    sx, sy, sz = size["x"], size["y"], size["z"]

    verts = [
        (-sx/2, -sy/2, -sz/2),
        ( sx/2, -sy/2, -sz/2),
        ( sx/2,  sy/2, -sz/2),
        (-sx/2,  sy/2, -sz/2),
        (-sx/2, -sy/2,  sz/2),
        ( sx/2, -sy/2,  sz/2),
        ( sx/2,  sy/2,  sz/2),
        (-sx/2,  sy/2,  sz/2),
    ]

    faces = [
        (0, 3, 2, 1),  # north
        (1, 2, 6, 5),  # east
        (4, 5, 6, 7),  # south
        (3, 0, 4, 7),  # west
        (0, 1, 5, 4),  # down
        (2, 3, 7, 6),  # up
    ]

    FACE_ORDER = ["north", "east", "south", "west", "down", "up"]

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    uv_layer = mesh.uv_layers.new(name="UVMap")
    uvs = uv_layer.data

    tex_width = 32
    tex_height = 32
    texture_layout = shape.get("textureLayout", {})

    # one face = 4 loops
    for face_index in range(len(FACE_ORDER)):
        face_name = FACE_ORDER[face_index]

        index = face_index * 4

        if face_name not in texture_layout:
            continue

        offset = texture_layout[face_name]["offset"]

        # derive face pixel size from box dimensions
        if face_name in ("north", "south"):
            face_w, face_h = sx, sy
        elif face_name in ("east", "west"):
            face_w, face_h = sz, sy
        else:  # up / down
            face_w, face_h = sx, sz

        ox = offset["x"]
        oy = offset["y"]

        # Blockbench-style conversion (top-left origin)
        top_left = (
            ox / tex_width,
            1.0 - oy / tex_height
        )
        bottom_right = (
            (ox + face_w) / tex_width,
            1.0 - (oy + face_h) / tex_height
        )

        uvs[index].uv     = (top_left[0], bottom_right[1])
        uvs[index + 1].uv = top_left
        uvs[index + 2].uv = (bottom_right[0], top_left[1])
        uvs[index + 3].uv = bottom_right

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj
