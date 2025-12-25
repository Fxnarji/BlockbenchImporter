import sys
import os
import bpy

# Add the 'res' folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "res"))

from operators.OBJECT_OT_Sample import OBJECT_OT_Sample

# Register operator
bpy.utils.register_class(OBJECT_OT_Sample)


def test_poll():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    ctx = bpy.context
    print("Poll without objects:", OBJECT_OT_Sample.poll(ctx))  # Expect False

    bpy.ops.mesh.primitive_cube_add()
    print("Poll with object:", OBJECT_OT_Sample.poll(ctx))  # Expect True


def test_execute():
    obj = bpy.context.active_object
    old_name = obj.name
    result = bpy.ops.object.operator()  # your bl_idname

    print("Execute result:", result)
    print("Object renamed:", obj.name)
    print("Old name:", old_name)


test_poll()
test_execute()

# Unregister
bpy.utils.unregister_class(OBJECT_OT_Sample)
