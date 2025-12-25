import bpy  # type: ignore
from ..constants import get_operator


# Define the operator to snap FK bones to IK bones
class OBJECT_OT_Sample(bpy.types.Operator):
    bl_idname = get_operator("operator")
    bl_description = "Renames selected Object to Hello World"
    bl_label = "Renames selected object to Hello World"
    bl_options = {"REGISTER", "UNDO"}

    # optional but handy: this will make sure the operator can only run when there is an active object
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = bpy.context.active_object
        self.report({"INFO"}, f"Renamed {obj.name} -> Hello World!")
        obj.name = "Hello World"
        return {"FINISHED"}
