import bpy
import math
from mathutils import Vector, Matrix

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def set_scene_units():
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 0.01  # 1 BU = 1 cm

def create_aluminum_material():
    material = bpy.data.materials.new(name="Aluminum Alloy")
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (0.91, 0.92, 0.93, 1)  # Light silver color
    principled_bsdf.inputs['Metallic'].default_value = 1.0
    principled_bsdf.inputs['Roughness'].default_value = 0.1  # More polished look
    principled_bsdf.inputs['IOR'].default_value = 1.39  # IOR for aluminum
    principled_bsdf.inputs['Anisotropic'].default_value = 0.1  # Slight anisotropic effect
    principled_bsdf.inputs['Specular IOR Level'].default_value = 0.5
    principled_bsdf.inputs['Coat Weight'].default_value = 0.1
    principled_bsdf.inputs['Coat Roughness'].default_value = 0.2
    return material

def create_gold_material():
    material = bpy.data.materials.new(name="Gold")
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (1.0, 0.843, 0.0, 1)  # Gold color
    principled_bsdf.inputs['Metallic'].default_value = 1.0
    principled_bsdf.inputs['Roughness'].default_value = 0.4
    return material

def create_exhaust_fluid_material():
    fluid_material = bpy.data.materials.new(name="Exhaust Fluid")
    fluid_material.use_nodes = True
    principled_bsdf = fluid_material.node_tree.nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # Dark gray color
    principled_bsdf.inputs['Metallic'].default_value = 0.0
    principled_bsdf.inputs['Roughness'].default_value = 1.0
    principled_bsdf.inputs['Transmission Weight'].default_value = 0.95
    principled_bsdf.inputs['IOR'].default_value = 1.0
    principled_bsdf.inputs['Alpha'].default_value = 0.1
    principled_bsdf.inputs['Subsurface Weight'].default_value = 0.5
    principled_bsdf.inputs['Subsurface Radius'].default_value = (0.5, 0.5, 0.5)
    principled_bsdf.inputs['Emission Color'].default_value = (1.0, 0.5, 0.0, 1)  # Orange color
    principled_bsdf.inputs['Emission Strength'].default_value = 0.5
    return fluid_material

def create_ceramic_material():
    material = bpy.data.materials.new(name="Ceramic")
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.95, 1)  # Light blue-gray color
    principled_bsdf.inputs['Metallic'].default_value = 0.0
    principled_bsdf.inputs['Roughness'].default_value = 0.2
    principled_bsdf.inputs['IOR'].default_value = 1.5  # Typical IOR for ceramics
    principled_bsdf.inputs['Specular IOR Level'].default_value = 0.5
    principled_bsdf.inputs['Sheen Weight'].default_value = 0.1
    principled_bsdf.inputs['Sheen Roughness'].default_value = 0.3
    principled_bsdf.inputs['Coat Weight'].default_value = 0.2
    principled_bsdf.inputs['Coat Roughness'].default_value = 0.1
    return material

def create_cast_iron_material():
    material = bpy.data.materials.new(name="Cast Iron")
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (0.01, 0.02, 0.03, 1)  # Dark gray color
    principled_bsdf.inputs['Metallic'].default_value = 0.8
    principled_bsdf.inputs['Roughness'].default_value = 0.7
    principled_bsdf.inputs['IOR'].default_value = 2.5  # Typical IOR for iron
    return material

def setup_camera():
    camera_data = bpy.data.cameras.new(name='Camera')
    camera = bpy.data.objects.new('Camera', camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    camera_data.clip_start = 0.1
    camera_data.clip_end = 1000
    camera.location = (70, -5, -100)
    camera.rotation_euler = (math.radians(180), math.radians(40), math.radians(180))

def setup_lighting():
    # Area Light
    light_data = bpy.data.lights.new(name='Area Light', type='AREA')
    light = bpy.data.objects.new('Area Light', light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0, -20, 50)
    light.data.energy = 1000
    light.data.size = 5
    direction = Vector((0, 0, 0)) - light.location
    rotation_matrix = Matrix.Rotation(math.radians(183), 4, 'Z')
    rotated_direction = rotation_matrix @ direction
    rot_quat = rotated_direction.to_track_quat('-Z', 'Y')
    light.rotation_euler = rot_quat.to_euler()

    # Sun Light
    sun_data = bpy.data.lights.new(name='Sun', type='SUN')
    sun = bpy.data.objects.new('Sun', sun_data)
    bpy.context.collection.objects.link(sun)
    sun.location = (10, 10, -50)
    direction = Vector((100, 100, 199))
    rotation_matrix = Matrix.Rotation(math.radians(180), 4, 'Z')
    rotated_direction = rotation_matrix @ direction
    rot_quat = rotated_direction.to_track_quat('-Z', 'Y')
    sun.rotation_euler = rot_quat.to_euler()
    sun.data.energy = 5.0

def set_render_settings():
    bpy.context.scene.render.engine = 'CYCLES'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.clip_start = 0.1
                    space.clip_end = 1000

def setup_world_environment():
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links

    world_nodes.clear()

    node_environment = world_nodes.new(type='ShaderNodeTexEnvironment')
    node_background = world_nodes.new(type='ShaderNodeBackground')
    node_output = world_nodes.new(type='ShaderNodeOutputWorld')

    world_links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    world_links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

    hdri_path = "/Users/wenweiwong/Projects/blender_scripting/engine/src/asset/lonely_road_afternoon_puresky_4k.exr" 
    node_environment.image = bpy.data.images.load(hdri_path)

def apply_transformations():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

def recalculate_normals():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')