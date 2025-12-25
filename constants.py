# i like to put values i need in multiple places here so i can change them in one place
import bpy  # type: ignore
import os
import tomllib


# has to be all lowercase
bl_id_prefix = "my_addon"

class AddonProperties:
    module_name = __package__
    panel_category = "SamplePanel"


def get_manifest():
    toml_path = os.path.join(os.path.dirname(__file__), "blender_manifest.toml")
    with open(toml_path, "rb") as f:
        manifest = tomllib.load(f)
    return manifest


def get_preferences():
    # No context needed, directly get addon preferences by package name
    addon_prefs = bpy.context.preferences.addons.get(__package__).preferences
    return addon_prefs


def get_operator(name):
    return bl_id_prefix + "." + name

