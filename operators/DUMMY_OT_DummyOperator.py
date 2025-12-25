import bpy  # type: ignore
from ..constants import get_operator


class DUMMY_OT_DummyOperator(bpy.types.Operator):
    bl_idname = get_operator("dummy")
    bl_label = "Dummy Operator"

    def execute(self, context):
        print("I did absolutely nothing!")
        return {"FINISHED"}

