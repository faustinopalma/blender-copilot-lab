"""An original coding cat with six tentacles; no external assets or official logo."""

import bpy
import json
import math
from mathutils import Vector


def material(name, color, metallic=0.0, roughness=0.35, glow=0.0):
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, 1.0)
    result.use_nodes = True
    shader = result.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    if glow:
        shader.inputs["Emission Color"].default_value = (*color, 1.0)
        shader.inputs["Emission Strength"].default_value = glow
    return result


def smooth(obj, name, mat):
    obj.name = name
    obj.data.materials.append(mat)
    if obj.type == "MESH":
        for polygon in obj.data.polygons:
            polygon.use_smooth = True
    return obj


def sphere(name, location, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=24, location=location
    )
    obj = smooth(bpy.context.object, name, mat)
    obj.scale = scale
    return obj


def tube(name, points, thickness, mat, radii=None):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 20
    data.bevel_depth = thickness
    data.bevel_resolution = 5
    data.use_fill_caps = True
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for index, (point, position) in enumerate(zip(spline.bezier_points, points)):
        point.co = position
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
        if radii is not None:
            point.radius = radii[index]
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def text(name, body, location, size, mat):
    data = bpy.data.curves.new(name, "FONT")
    data.body = body
    data.align_x = "CENTER"
    data.size = size
    data.extrude = 0.008
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.pi / 2, 0, 0)
    data.materials.append(mat)
    return obj


def ear(name, side, mat):
    vertices = [
        (side * 0.45, -0.38, 4.12),
        (side * 1.28, -0.26, 4.08),
        (side * 1.12, -0.12, 5.17),
        (side * 0.45, 0.28, 4.12),
        (side * 1.28, 0.32, 4.08),
        (side * 1.12, 0.20, 5.17),
    ]
    faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3),
             (1, 2, 5, 4), (2, 0, 3, 5)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    smooth(obj, name, mat)
    bevel = obj.modifiers.new("Soft toy edges", "BEVEL")
    bevel.width = 0.13
    bevel.segments = 4
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj


def point_at(obj, location):
    obj.rotation_euler = (Vector(location) - obj.location).to_track_quat("-Z", "Y").to_euler()


def build_scene():
    if bpy.context.scene.get("blender_mcp_lab") != "disposable-test":
        raise RuntimeError("Refusing to replace a scene outside the disposable Blender lab")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.data.orphans_purge(do_recursive=True)
    scene = bpy.context.scene
    scene.name = "Coding Cat - original study"
    scene["original_design"] = True
    scene["external_assets"] = 0
    scene["expected_tentacles"] = 6
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 48
    scene.view_settings.view_transform = "AgX"
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.025, 0.045, 0.085, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
    scene.render.use_file_extension = True

    ink = material("Midnight enamel", (0.018, 0.032, 0.065), 0.25, 0.27)
    face = material("Warm porcelain", (0.94, 0.71, 0.52), 0.0, 0.46)
    teal = material("Lagoon accent", (0.025, 0.65, 0.64), 0.20, 0.3)
    glow = material("Mint light", (0.08, 0.9, 0.76), 0.2, 0.25, 2.0)
    eye = material("Obsidian eyes", (0.004, 0.008, 0.018), 0.05, 0.18)
    white = material("Eye sparkle", (0.96, 0.99, 1.0), 0, 0.22, 0.2)
    pink = material("Coral nose", (0.92, 0.22, 0.27), 0, 0.45)
    gold = material("Amber satellite", (0.95, 0.42, 0.09), 0.5, 0.26)
    stage = material("Stage graphite", (0.035, 0.06, 0.10), 0.55, 0.3)
    floor = material("Studio navy", (0.035, 0.055, 0.09), 0, 0.6)

    sphere("Cat torso", (0, 0.08, 1.9), (0.77, 0.65, 0.97), ink)
    sphere("Cat head", (0, 0, 3.55), (1.32, 0.88, 1.13), ink)
    ear("Ear L", -1, ink)
    ear("Ear R", 1, ink)
    for side in (-1, 1):
        sphere("Inner ear " + str(side), (side * 1.0, -0.35, 4.55), (0.17, 0.055, 0.29), teal)
    sphere("Face mask", (0, -0.77, 3.49), (1.055, 0.215, 0.82), face)
    for side in (-1, 1):
        sphere("Eye " + str(side), (side * 0.43, -0.976, 3.66), (0.205, 0.083, 0.285), eye)
        sphere("Sparkle " + str(side), (side * 0.43 - 0.055, -1.05, 3.77), (0.063, 0.026, 0.075), white)
        sphere("Cheek " + str(side), (side * 0.72, -0.96, 3.28), (0.17, 0.025, 0.08), pink)
        for index in range(2):
            z = 3.32 + index * 0.19
            tube("Whisker " + str(side) + " " + str(index),
                 [(side * 0.85, -0.94, z),
                  (side * 1.16, -0.91, z + 0.04),
                  (side * 1.43, -0.86, z + 0.10)], 0.019, ink)
    sphere("Nose", (0, -1.01, 3.39), (0.105, 0.055, 0.075), pink)
    tube("Smile", [(-0.22, -0.98, 3.20), (0, -1.002, 3.13),
                   (0.22, -0.98, 3.20)], 0.023, ink)
    sphere("Coder badge", (0, -0.55, 2.04), (0.47, 0.13, 0.40), teal)
    text("Terminal glyph", ">_", (0, -0.691, 1.96), 0.27, white)

    for index in range(6):
        angle = math.radians(-165 + index * 60)
        dx, dy = math.cos(angle), math.sin(angle)
        points = [
            (dx * 0.44, dy * 0.44, 1.45),
            (dx * 0.95, dy * 0.95, 0.67),
            (dx * 1.70, dy * 1.70, 0.57),
            (dx * 2.05 - dy * 0.18, dy * 2.05 + dx * 0.18, 0.82),
            (dx * 1.99 - dy * 0.38, dy * 1.99 + dx * 0.38, 1.13),
        ]
        tube("Tentacle " + str(index + 1).zfill(2), points, 0.26, ink,
             [1.0, 1.0, 0.80, 0.59, 0.25])
        sphere("Tentacle tip " + str(index + 1).zfill(2), points[-1],
               (0.075, 0.075, 0.095), teal)
        for suction in range(3):
            radius = 1.1 + suction * 0.23
            sphere("Sucker " + str(index) + " " + str(suction),
                   (dx * radius, dy * radius, 0.77),
                   (0.07, 0.07, 0.04), teal)

    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=2.62, depth=0.28,
                                       location=(0, 0, 0.25))
    pedestal = smooth(bpy.context.object, "Display plinth", stage)
    bevel = pedestal.modifiers.new("Machined rim", "BEVEL")
    bevel.width = 0.09
    bevel.segments = 4
    bpy.ops.mesh.primitive_torus_add(major_radius=2.50, minor_radius=0.032,
                                    major_segments=128, minor_segments=16,
                                    location=(0, 0, 0.41))
    smooth(bpy.context.object, "Status ring", glow)
    text("Plinth label", "HELLO, HUMAN", (0, -2.626, 0.21), 0.16, glow)
    for index, (location, radius) in enumerate([
        ((-2.05, 0.35, 3.2), 0.13), ((2.0, 0.40, 4.15), 0.17),
        ((1.8, 0.35, 2.8), 0.075),
    ]):
        sphere("Floating bit " + str(index), location, (radius, radius, radius),
               gold if index == 1 else teal)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0.065))
    smooth(bpy.context.object, "Studio floor", floor)

    bpy.ops.object.camera_add(location=(6.0, -12.5, 6.9))
    camera = bpy.context.object
    camera.name = "Portrait camera"
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 7.5
    point_at(camera, (0, 0, 2.45))
    scene.camera = camera
    for name, location, energy, color, size in [
        ("Key softbox", (2, -6, 8), 1400, (0.80, 0.91, 1.0), 5.0),
        ("Warm fill", (-5, -2, 4), 1100, (1.0, 0.70, 0.48), 4.0),
        ("Teal rim", (3, 4, 7), 2000, (0.27, 1.0, 0.88), 3.5),
    ]:
        bpy.ops.object.light_add(type="AREA", location=location)
        lamp = bpy.context.object
        lamp.name = name
        lamp.data.energy = energy
        lamp.data.color = color
        lamp.data.shape = "DISK"
        lamp.data.size = size
        point_at(lamp, (0, 0, 2.5))
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = bpy.data.objects["Cat head"]
    bpy.data.objects["Cat head"].select_set(True)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"
                area.spaces.active.shading.type = "MATERIAL"
    bpy.context.view_layer.update()
    print("SCENE_BUILT=" + json.dumps({
        "objects": len(scene.objects), "tentacles": 6,
        "engine": scene.render.engine, "version": bpy.app.version_string
    }))


build_scene()
