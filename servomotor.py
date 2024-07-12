import bpy
from math import radians

def create_cube(name, dimensions, location):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=location)
    cube = bpy.context.active_object
    cube.name = name
    cube.dimensions = dimensions
    return cube

def create_cylinder(name, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, enter_editmode=False, location=location)
    cylinder = bpy.context.active_object
    cylinder.name = name
    cylinder.rotation_euler = [radians(angle) for angle in rotation]
    return cylinder

def create_sg90_servo(location, rotation=(0, 0, 0)):
    # Create the main body
    body = create_cube("Servo_Body", (0.0122, 0.0225, 0.0225), location)
    body.rotation_euler = [radians(angle) for angle in rotation]
    
    # Create the mounting tabs
    tab1 = create_cube("Mounting_Tab_1", (0.0025, 0.0322, 0.0025), (location[0], location[1], location[2] - 0.01))
    tab1.rotation_euler = [radians(angle) for angle in rotation]

    tab2 = create_cube("Mounting_Tab_2", (0.0025, 0.0322, 0.0025), (location[0], location[1], location[2] + 0.01))
    tab2.rotation_euler = [radians(angle) for angle in rotation]

    # Create the shaft
    shaft = create_cylinder("Servo_Shaft", 0.00235, 0.004, (location[0], location[1], location[2] + 0.01325))
    shaft.rotation_euler = [radians(angle) for angle in rotation]

    # Create the horn
    horn = create_cylinder("Servo_Horn", 0.0035, 0.0015, (location[0], location[1], location[2] + 0.0155))
    horn.rotation_euler = [radians(angle) for angle in rotation]

    # Group all parts
    servo_parts = [body, tab1, tab2, shaft, horn]
    servo_group = bpy.data.collections.new("SG90_Servo_" + str(location))
    bpy.context.scene.collection.children.link(servo_group)
    for part in servo_parts:
        bpy.context.scene.collection.objects.link(part)
        bpy.context.scene.collection.objects.unlink(part)
        servo_group.objects.link(part)
    
    return servo_parts

def create_leg(name, base_location):
    # Create the hip servo
    hip_servo_parts = create_sg90_servo(base_location, (90, 0, 0))
    
    # Create the upper leg segment
    upper_leg = create_cube(name + "_Upper_Leg", (0.02, 0.02, 0.1), (base_location[0], base_location[1], base_location[2] - 0.1))
    
    # Create the knee servo
    knee_servo_location = (base_location[0], base_location[1], base_location[2] - 0.2)
    knee_servo_parts = create_sg90_servo(knee_servo_location, (90, 0, 0))
    
    # Create the lower leg segment
    lower_leg = create_cube(name + "_Lower_Leg", (0.02, 0.02, 0.1), (knee_servo_location[0], knee_servo_location[1], knee_servo_location[2] - 0.1))
    
    # Create the foot servo
    foot_servo_location = (knee_servo_location[0], knee_servo_location[1], knee_servo_location[2] - 0.2)
    foot_servo_parts = create_sg90_servo(foot_servo_location, (90, 0, 0))
    
    # Create the foot segment
    foot = create_cube(name + "_Foot", (0.04, 0.02, 0.02), (foot_servo_location[0], foot_servo_location[1], foot_servo_location[2] - 0.02))
    
    # Group all parts of the leg
    leg_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(leg_group)
    
    all_parts = hip_servo_parts + [upper_leg] + knee_servo_parts + [lower_leg] + foot_servo_parts + [foot]
    for part in all_parts:
        bpy.context.scene.collection.objects.link(part)
        bpy.context.scene.collection.objects.unlink(part)
        leg_group.objects.link(part)


# Create the first leg
create_leg("Left_Leg", (0.1, 0, 0.5))

# Create the second leg
create_leg("Right_Leg", (-0.1, 0, 0.5))

print("Two robot legs with 3 SG90 servos each created successfully and ready for individual movement")