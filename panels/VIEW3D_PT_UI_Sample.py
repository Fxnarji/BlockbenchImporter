import bpy  # type: ignore
from ..constants import AddonProperties
from ..operators.OBJECT_OT_Sample import OBJECT_OT_Sample

class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    bl_label = "A Fancy Panel!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_Sample.bl_idname, text="example operator", icon="BLENDER")

