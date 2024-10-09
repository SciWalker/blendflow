import bpy
import math
from mathutils import Vector
import os
import sys
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
def create_main_engine_body(engine_diameter, engine_length):
    print("Creating main engine body")
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=128,
        radius=engine_diameter / 2,
        depth=engine_length,
        location=(0, 0, 0)
    )
    main_body = bpy.context.active_object
    main_body.name = "Engine Body"
    return main_body

def create_air_inlet(engine_diameter, engine_length):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=128,
        radius=5,
        depth=14,
        location=(0, -(engine_diameter / 2 + 5), -engine_length / 4)
    )
    air_inlet = bpy.context.active_object
    air_inlet.rotation_euler = (math.radians(90), 0, 0)
    air_inlet.name = "Air Inlet"

def create_shaft_holder(engine_length):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=3,
        depth=8,
        location=(0, 0, engine_length / 2 - 38)
    )
    shaft_holder = bpy.context.active_object
    shaft_holder.name = "Shaft Holder"

def create_power_shaft(engine_length):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=2,
        depth=10,
        location=(0, 0, engine_length / 2 - 39)
    )
    power_shaft = bpy.context.active_object
    power_shaft.name = "Power Shaft"

def create_seal(engine_length):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=2.5,
        minor_radius=0.5,
        location=(0, 0, engine_length / 2 + 5)
    )
    seal = bpy.context.active_object
    seal.name = "Seal"

def create_bolt_assembly(engine_diameter, engine_length):
    num_bolts = 8
    bolt_radius = 0.5
    bolt_depth = 3
    bolt_distance = engine_diameter / 2 - 0.5

    for i in range(num_bolts):
        angle = i * (2 * math.pi / num_bolts)
        x = bolt_distance * math.cos(angle)
        y = bolt_distance * math.sin(angle)
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=bolt_radius,
            depth=bolt_depth,
            location=(x, y, -engine_length / 2 + bolt_depth / 2 - 0.5)
        )
        bolt = bpy.context.active_object
        bolt.name = f"Bolt_{i+1}"
        
        direction = Vector((x, y, 0)).normalized()
        rot_angle = math.atan2(direction.y, direction.x) + math.pi / 2
        bolt.rotation_euler = (0, 0, rot_angle)

def create_exhaust_holes(engine_diameter, engine_length):
    num_holes = 10
    hole_width = 1
    hole_height = 2
    hole_length = engine_diameter * 2
    hole_objects = []

    for i in range(num_holes):
        z_position = -(engine_length-4) / 2 + (i + 0.5) * ((engine_length-4) / num_holes)
        x_position = engine_diameter / 2 - hole_height / 2
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_position, 0, z_position)
        )
        hole = bpy.context.active_object
        hole.scale = (hole_length, hole_width, hole_height)
        hole.name = f"Exhaust_Hole_{i+1}"
        hole_objects.append(hole)

    return hole_objects

def join_holes(hole_objects):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in hole_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = hole_objects[0]
    bpy.ops.object.join()
    return hole_objects[0]

def create_holes_in_main_body(main_body, holes_union):
    bpy.ops.object.select_all(action='DESELECT')
    main_body.select_set(True)
    bpy.context.view_layer.objects.active = main_body
    bool_mod = main_body.modifiers.new(type="BOOLEAN", name="Exhaust_Holes")
    bool_mod.object = holes_union
    bool_mod.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(holes_union, do_unlink=True)

def create_exhaust_fluid(engine_diameter, engine_length):
    num_fluids = 10
    fluid_width = 3
    fluid_height = 2.5
    fluid_length = engine_diameter * 1
    
    for i in range(num_fluids):
        z_position = -(engine_length-4) / 2 + (i + 0.5) * ((engine_length-4) / num_fluids)
        x_position = engine_diameter / 2 + fluid_length / 2
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_position, 0, z_position)
        )
        fluid = bpy.context.active_object
        fluid.scale = (fluid_length, fluid_width, fluid_height)
        fluid.name = f"Exhaust_Fluid_{i+1}"

        # Add displacement modifier for more organic shape
        displace_mod = fluid.modifiers.new(name="Displace", type='DISPLACE')
        texture = bpy.data.textures.new("Fluid_Texture", type='CLOUDS')
        texture.noise_scale = 0.5
        displace_mod.texture = texture
        displace_mod.strength = 0.66

        # Add subdivision surface modifier for smoother appearance
        subdiv_mod = fluid.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv_mod.levels = 2
        subdiv_mod.render_levels = 2

    # Create domain for fluid simulation
    bpy.ops.mesh.primitive_cube_add(size=1)
    domain = bpy.context.active_object
    domain.name = "Fluid_Domain"
    domain.scale = (engine_diameter * 2, engine_diameter * 2, engine_length * 1.5)
    domain.location = (engine_diameter, 0, 0)

    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain.modifiers["Fluid"].domain_settings.resolution_max = 64
    domain.modifiers["Fluid"].domain_settings.use_adaptive_domain = True