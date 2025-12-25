import bpy  # type: ignore

# preferences
from .preferences import Sample_Preferences

# Operators
from .operators.OBJECT_OT_Sample import OBJECT_OT_Sample
from .operators.DUMMY_OT_DummyOperator import DUMMY_OT_DummyOperator

# panels
from .panels.VIEW3D_PT_UI_Sample import VIEW3D_PT_UI_Sample


# reading values such as name, version and more from toml so there is no need to change information in two places
def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()

    # reading addon name
    extension_name = manifest["name"]

    # reading addon version
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

    # reading Blender version
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

    bl_info = {
        "name": extension_name,
        "version": version_tuple,
        "blender": blender_version_tuple,
    }

    return bl_info


blender_manifest = load_manifest_info()
bl_info = {
    "name": blender_manifest["name"],
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Your Name",
    "version": blender_manifest["version"],
    "blender": blender_manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
    # preferences
    Sample_Preferences,
    # operators:
    OBJECT_OT_Sample,
    DUMMY_OT_DummyOperator,
    # panels:
    VIEW3D_PT_UI_Sample,
]


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in reversed(classes):
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()

