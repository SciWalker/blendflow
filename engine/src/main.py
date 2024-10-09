import bpy
import sys
import os

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import engine_parts
from scene_setup import *
from importlib import reload

reload(engine_parts)
reload(sys.modules['scene_setup'])

def main():
    engine_diameter = 20  # cm
    engine_length = 40    # cm
    bpy.context.scene.unit_settings.system = 'METRIC'
    print("Starting engine creation")
    bpy.context.scene.unit_settings.system = 'METRIC'
    clear_scene()
    set_scene_units()
    main_body = engine_parts.create_main_engine_body(engine_diameter, engine_length)
    engine_parts.create_air_inlet(engine_diameter, engine_length)
    shaft_holder = engine_parts.create_shaft_holder(engine_length)
    power_shaft = engine_parts.create_power_shaft(engine_length)
    engine_parts.create_seal(engine_length)
    engine_parts.create_bolt_assembly(engine_diameter, engine_length)
    engine_parts.create_exhaust_fluid(engine_diameter, engine_length)  

    material = bpy.data.materials.new(name="Gold")
    hole_objects = engine_parts.create_exhaust_holes(engine_diameter, engine_length)
    holes_union = engine_parts.join_holes(hole_objects)
    engine_parts.create_holes_in_main_body(main_body, holes_union)
    # Create materials
    aluminum_material = create_aluminum_material()
    gold_material = create_gold_material()
    exhaust_fluid_material = create_exhaust_fluid_material()
    ceramic_material = create_ceramic_material()
    cast_iron_material = create_cast_iron_material()
    # Assign materials
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if obj.name == "Engine Body":
                obj.data.materials.clear()
                obj.data.materials.append(cast_iron_material)
            elif obj.name == "Air Inlet":
                obj.data.materials.clear()
                obj.data.materials.append(gold_material)
                obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.9, 1)  # Bright metal color
            elif obj.name == "Power Shaft":
                obj.data.materials.clear()
                obj.data.materials.append(ceramic_material)
            elif obj.name == "Shaft Holder":
                obj.data.materials.clear()
                shaft_holder_material = ceramic_material.copy()
                shaft_holder_material.name = "Shaft Holder Material"
                obj.data.materials.append(shaft_holder_material)
                obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0, 0.105, 0.298, 1)  # Marine blue color
#

            elif obj.name.startswith("Exhaust_Fluid"):

                obj.data.materials.clear()
                obj.data.materials.append(exhaust_fluid_material)
            else:
                obj.data.materials.clear()
                obj.data.materials.append(aluminum_material)
    # Area Light
    setup_camera()
    setup_lighting()
    setup_world_environment()
    set_render_settings()
    apply_transformations()
    recalculate_normals()

if __name__ == "__main__":
    main()